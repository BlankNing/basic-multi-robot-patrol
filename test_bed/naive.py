import matplotlib.pyplot as plt
import numpy as np


# Class representing a Node
class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.refresh_time = 0

    def increment_refresh_time(self, time_step):
        self.refresh_time += time_step

    def reset_refresh_time(self):
        self.refresh_time = 0

# MSP
# Class representing a Robot
class Robot:
    def __init__(self, robot_id, patrol_nodes, slow_start=200):
        self.robot_id = robot_id
        self.patrol_nodes = patrol_nodes
        self.slow_start = slow_start  # The time at which the robot slows down

    def visit_node(self, current_time, patrol_period, slow_patrol_period=None):
        # If the robot is past the slow_start time, use the slower patrol period
        if current_time >= self.slow_start and slow_patrol_period is not None:
            patrol_period = slow_patrol_period

        patrol_cycle = patrol_period // len(self.patrol_nodes)
        v_flag = False
        if current_time % patrol_cycle == 0:
            v_flag = True
        index = (current_time // patrol_cycle) % len(self.patrol_nodes)
        return [self.patrol_nodes[index], v_flag]


# Class representing the Central Monitor
class CentralMonitor:
    def __init__(self, robots, time_step, total_time, slow_patrol_period=None):
        self.robots = robots
        self.time_step = time_step
        self.total_time = total_time
        self.slow_patrol_period = slow_patrol_period
        self.time_series = np.arange(0, self.total_time, self.time_step)
        self.node_data = {node.node_id: [] for node in [n for r in robots for n in r.patrol_nodes]}

    def simulate(self):
        for t in self.time_series:
            # Increment refresh times for all nodes
            for robot in self.robots:
                for node in robot.patrol_nodes:
                    node.increment_refresh_time(self.time_step)

            # Robots visit their respective nodes, staying only for one timestep
            patrol_period = 80  # Normal patrol period
            for robot in self.robots:
                slow_patrol_period = None
                if robot.robot_id == 0:  # The poorly performing robot
                    slow_patrol_period = 240  # Slower patrol period after 200 timesteps

                visited_node, v_flag = robot.visit_node(
                    t, patrol_period, slow_patrol_period
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


# Initialize Nodes and Robots
nodes = [Node(i) for i in range(32)]  # 32 nodes for 8 robots, each with 4 nodes

robots = [
    Robot(i, nodes[i * 4: (i + 1) * 4]) for i in range(8)
]

# Create Central Monitor and simulate with a total of 1000 timesteps
central_monitor = CentralMonitor(robots, 1, 2000)  # 1-second time step, total 1000 seconds
central_monitor.simulate()

# Plot the results for a normal node and the poorly performing node
normal_node_id = 0  # A normal node
poorly_performing_node_id = 5  # A node from the poorly performing robot's patrol area

central_monitor.plot([normal_node_id, poorly_performing_node_id])
