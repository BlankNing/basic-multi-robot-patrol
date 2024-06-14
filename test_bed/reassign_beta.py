import matplotlib.pyplot as plt
import numpy as np
from config import (
    TOTAL_NODES,
    NUM_ROBOTS,
    NODES_PER_ROBOT,
    BASE_PATROL_PERIOD,
    SLOW_PATROL_PERIOD,
    SLOW_START,
    TIME_STEP,
    TOTAL_TIME,
    REASSIGNMENT_TIME,
    REASSIGN_FROM_ROBOT,
    REASSIGN_TO_ROBOT,
    REASSIGN_NODE_ID,
    TRUST_THRESHOLD,
)

# Class representing a Node
class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.refresh_time = 0

    def increment_refresh_time(self, time_step):
        self.refresh_time += time_step

    def reset_refresh_time(self):
        self.refresh_time = 0


# Class representing a Robot
class Robot:
    def __init__(self, robot_id, patrol_nodes, slow_start=SLOW_START):
        self.robot_id = robot_id
        self.patrol_nodes = patrol_nodes
        self.slow_start = slow_start
        self.alpha = 0
        self.beta = 0

    def get_patrol_period(self, current_time):
        # Determine patrol period based on node count and slow down after a specific time
        patrol_period = BASE_PATROL_PERIOD * len(self.patrol_nodes)
        if current_time >= self.slow_start and self.robot_id == 0:
            patrol_period = SLOW_PATROL_PERIOD * len(self.patrol_nodes)
        return patrol_period

    def update_patrol_counts(self, current_time):
        patrol_period = self.get_patrol_period(current_time)
        if patrol_period == BASE_PATROL_PERIOD * len(self.patrol_nodes):
            self.alpha += 1  # Base patrol
        else:
            self.beta += 1  # Slow patrol

    def get_trust(self):
        # Trust calculated from the beta distribution
        return (self.alpha + 1) / (self.alpha + self.beta + 2)

    def visit_node(self, current_time, patrol_period):
        # Calculate the patrol cycle based on current patrol period
        patrol_cycle = patrol_period // len(self.patrol_nodes)
        v_flag = False
        if current_time % patrol_cycle == 0:
            v_flag = True
        index = (current_time // patrol_cycle) % len(self.patrol_nodes)
        return [self.patrol_nodes[index], v_flag]


# Class representing the Central Monitor
class CentralMonitor:
    def __init__(self, robots):
        self.robots = robots
        self.time_step = TIME_STEP
        self.total_time = TOTAL_TIME
        self.time_series = np.arange(0, self.total_time, self.time_step)
        self.node_data = {node.node_id: [] for node in [n for r in robots for n in r.patrol_nodes]}
        self.trust_data = {robot.robot_id: [] for robot in robots}
        self.re_flag = False

    def reassign_node(self):
        from_robot = self.robots[REASSIGN_FROM_ROBOT]
        to_robot = self.robots[REASSIGN_TO_ROBOT]

        node_to_reassign = None
        for node in from_robot.patrol_nodes:
            if node.node_id == REASSIGN_NODE_ID:
                node_to_reassign = node
                break

        if node_to_reassign:
            from_robot.patrol_nodes.remove(node_to_reassign)
            to_robot.patrol_nodes.append(node_to_reassign)

    def simulate(self):
        for t in self.time_series:
            # Trigger reassignment based on trust threshold
            for robot in self.robots:
                if robot.get_trust() < TRUST_THRESHOLD and not self.re_flag:
                    # Trigger task reassignment if trust falls below the threshold
                    self.reassign_node()  # Adjust with the correct robot and node ID
                    self.re_flag = True
                    print(robot.robot_id,'is not trust worthy, reassign robot 0\'s node 3 to robot 1')

            # Update patrol counts for each robot to calculate trust
            for robot in self.robots:
                robot.update_patrol_counts(t)
                self.trust_data[robot.robot_id].append(robot.get_trust())

            # Increment refresh times for all nodes
            for robot in self.robots:
                for node in robot.patrol_nodes:
                    node.increment_refresh_time(self.time_step)

            # Robots visit their respective nodes, staying only for one timestep
            for robot in self.robots:
                patrol_period = robot.get_patrol_period(t)

                visited_node, v_flag = robot.visit_node(
                    t, patrol_period
                )
                if v_flag:
                    visited_node.reset_refresh_time()

            # Collect data for plotting
            for node_id, node_list in self.node_data.items():
                # Find the node with the matching ID
                for robot in self.robots:
                    for node in robot.patrol_nodes:
                        if node.node_id == node_id:
                            node_list.append(node.refresh_time)

    def plot(self, node_ids):
        # Plot the refresh times for the specified nodes over time
        plt.figure(figsize=(12, 6))
        for node_id in node_ids:
            plt.plot(self.time_series, self.node_data[node_id], label=f'Node {node_id}')

        plt.xlabel('Time (s)')
        plt.ylabel('Refresh Time (s)')
        plt.title(f'Refresh Time of Nodes over Time')
        plt.legend()
        plt.show()

    def plot_robot_trust(self):
        plt.figure(figsize=(12, 6))
        for robot_id, trust_values in self.trust_data.items():
            plt.plot(self.time_series, trust_values, label=f'Robot {robot_id}')

        plt.xlabel('Time (s)')
        plt.ylabel('Trust')
        plt.title('Trust Values of Robots over Time')
        plt.legend()
        plt.show()

# Initialize Nodes and Robots
nodes = [Node(i) for i in range(TOTAL_NODES)]  # Total number of nodes

robots = [
    Robot(i, nodes[i * NODES_PER_ROBOT: (i + 1) * NODES_PER_ROBOT]) for i in range(NUM_ROBOTS)
]

# Create Central Monitor and simulate with a total of 2000 timesteps
central_monitor = CentralMonitor(robots)
central_monitor.simulate()

# Plot the results for the reassigned node and its neighbor's node
reassigned_node_id = REASSIGN_NODE_ID
neighbor_node_id = 4  # A node from robot 1's original patrol area

central_monitor.plot([reassigned_node_id, neighbor_node_id])

# Plot trust values for all robots
central_monitor.plot_robot_trust()