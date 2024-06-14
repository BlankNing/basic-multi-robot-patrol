import numpy as np
import matplotlib.pyplot as plt
import random

class Robot:
    def __init__(self, start_position, speed, connections):
        self.current_node = start_position
        self.position = 0  # Initialize the relative position to 0
        self.speed = speed
        self.connections = connections
        self.next_node = self.choose_next_node()

    def choose_next_node(self):
        return random.choice(self.connections[self.current_node])

    def move(self, current_step, speed_change_step, new_speed):
        if current_step >= speed_change_step:
            self.speed = new_speed
        self.position += self.speed
        if self.position >= 120:
            self.current_node = self.next_node
            self.position = 0
            self.next_node = self.choose_next_node()

def read_connections(filename):
    connections = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            node = int(parts[0])
            neighbors = list(map(int, parts[1].split()))
            connections[node] = neighbors
    return connections

def simulate(num_robots, num_nodes, speed, steps, speed_change_step, new_speed, connections):
    nodes = np.zeros(num_nodes)
    robots = [Robot(start_position=i * 4 % num_nodes, speed=speed, connections=connections) for i in range(num_robots)]
    idleness = np.zeros((steps, num_nodes))
    max_idleness_over_time = np.zeros(steps)

    for t in range(steps):
        # add idleness
        for node in range(num_nodes):
            idleness[t, node] = nodes[node]
            nodes[node] += 1

        for i, robot in enumerate(robots):
            if i == 2:
                robot.move(t, speed_change_step, new_speed)
            else:
                robot.move(t, steps, speed)
            # reset idleness
            if robot.position == 0:
                nodes[robot.current_node] = 0

        # record max idleness
        max_idleness_over_time[t] = np.max(nodes)

    return idleness, max_idleness_over_time

# 读取节点连接关系
connections = read_connections('connection.txt')

# 固定随机种子
random.seed(42)
np.random.seed(42)

# 参数设置
num_robots = 8
num_nodes = 32
speed = 6
steps = 1000
speed_change_step = 400
new_speed = 2

# 运行模拟
idleness, max_idleness_over_time = simulate(num_robots, num_nodes, speed, steps, speed_change_step, new_speed, connections)

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

plot_idleness([0])
plot_max_idleness_over_time(max_idleness_over_time)
