import numpy as np
import matplotlib.pyplot as plt
import random

class Robot:
    def __init__(self, start_position, speed, num_nodes):
        self.position = start_position * 120
        self.speed = speed
        self.num_nodes = num_nodes
        self.next_node = (start_position + 1) % num_nodes
        self.direction = 1  # 1 means moving to next node, -1 means moving to previous node

    def move(self, current_step, speed_change_step, new_speed):
        if current_step >= speed_change_step:
            self.speed = new_speed
        self.position += self.speed * self.direction
        if self.position == self.next_node * 120:
            # Decide next direction
            if random.random() < 0.5:
                self.direction *= -1
            self.next_node = (self.next_node + self.direction) % self.num_nodes
            if self.next_node < 0:
                self.next_node += self.num_nodes
            if self.next_node == 0 and self.direction == -1:
                self.position = self.num_nodes * 120

def simulate(num_robots, num_nodes, speed, steps, speed_change_step, new_speed):
    nodes = np.zeros(num_nodes)
    robots = [Robot(start_position=i * 4, speed=speed, num_nodes=num_nodes) for i in range(num_robots)]
    idleness = np.zeros((steps, num_nodes))
    max_idleness_over_time = np.zeros(steps)

    for t in range(steps):
        print(f'Step {t}:')
        # add idleness
        for node in range(num_nodes):
            idleness[t, node] = nodes[node]
            nodes[node] += 1

        for i, robot in enumerate(robots):
            if i == 2:
                robot.move(t, speed_change_step, new_speed)
                print(f'Robot{i} at position {robot.position}')

            else:
                robot.move(t, steps, speed)

            # reset idleness
            if robot.position % 120 == 0:
                node_index = int(robot.position / 120) % num_nodes
                nodes[node_index] = 0

        # record max idleness
        max_idleness_over_time[t] = np.max(nodes)

    return idleness, max_idleness_over_time

# parameter
num_robots = 8
num_nodes = 32
speed = 6
steps = 2000
speed_change_step = 400
new_speed = 0

#com

# random seed
random.seed(42)
np.random.seed(42)

# simulate
idleness, max_idleness_over_time = simulate(num_robots, num_nodes, speed, steps, speed_change_step, new_speed)

# 绘制结果
def plot_idleness(pts):
    plt.figure(figsize=(12, 6))
    for node in pts:
        plt.plot(idleness[:, node], label=f'Node {node}')
    plt.xlabel('Time Steps')
    plt.ylabel('Idleness')
    plt.title('Idleness of Each Node Over Time')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()

def plot_max_idleness_over_time(max_idleness_over_time):
    plt.figure(figsize=(12, 6))
    plt.plot(max_idleness_over_time, label='Max Idleness')
    plt.xlabel('Time Steps')
    plt.ylabel('Max Idleness')
    plt.title('Max Idleness of All Nodes Over Time')
    plt.legend()
    plt.show()

pts = [i for i in range(num_nodes)]
plot_idleness([0])
plot_max_idleness_over_time(max_idleness_over_time)
