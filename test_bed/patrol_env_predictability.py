import numpy as np
import matplotlib.pyplot as plt

# 定义邻接矩阵
n_points = 32
adj_matrix = np.zeros((n_points, n_points))

# 根据图中的连线更新邻接矩阵（此处的距离为假设值，请根据实际情况调整）
for i in range(0, n_points, 4):
    adj_matrix[i][i+1] = adj_matrix[i+1][i] = 1  # l
    adj_matrix[i+1][i+2] = adj_matrix[i+2][i+1] = 1  # h
    adj_matrix[i+2][i+3] = adj_matrix[i+3][i+2] = 1  # l
    if i < n_points - 4:
        adj_matrix[i+3][i+4] = adj_matrix[i+4][i+3] = 1  # d

# 打印邻接矩阵
print("adjacency matrix：")
print(adj_matrix)

# 初始化机器人位置、idleness和随机策略状态
robots_positions = [i * 4 for i in range(8)]  # 每个机器人初始位置
idleness = np.zeros(n_points)
time_steps = 1000
robots_flags = np.zeros(8, dtype=bool)  # 记录每个机器人是否刚到达一个点
random_mode = np.zeros(8, dtype=int)  # 记录每个机器人是否在随机模式下
random_mode_steps = np.zeros(8, dtype=int)  # 记录每个机器人在随机模式下还剩多少步
robots_speeds = np.full(8, 20)  # 每个机器人的速度固定为20个时间步
robots_remaining_steps = np.zeros(8, dtype=int)  # 记录每个机器人到达下一个点还需要多少步
next_positions = np.zeros(8, dtype=int)  # 记录每个机器人的下一个目标位置

# 顺序访问的下一个点
def get_next_pos(current_pos):
    neighbors = np.where(adj_matrix[current_pos] > 0)[0]
    return neighbors[0]  # 顺序选择下一个点

# 更新函数
def update_positions(robots_positions, random_mode, random_mode_steps, robots_remaining_steps, next_positions, robots_speeds):
    for i in range(len(robots_positions)):
        if robots_remaining_steps[i] > 0:
            robots_remaining_steps[i] -= 1
            robots_flags[i] = False
            if robots_remaining_steps[i] == 0:
                robots_positions[i] = next_positions[i]
                robots_flags[i] = True
        else:
            current_pos = robots_positions[i]
            if random_mode[i] > 0:
                neighbors = np.where(adj_matrix[current_pos] > 0)[0]
                new_pos = np.random.choice(neighbors)
                random_mode_steps[i] -= 1
                if random_mode_steps[i] == 0:
                    random_mode[i] = 0
            else:
                new_pos = get_next_pos(current_pos)
                #todo: change prob
                if np.random.rand() < 0.5:
                    random_mode[i] = 1
                    random_mode_steps[i] = 10
            robots_remaining_steps[i] = robots_speeds[i]
            next_positions[i] = new_pos
    return robots_positions, random_mode, random_mode_steps, robots_remaining_steps, next_positions, robots_flags

def update_idleness(idleness, robots_positions, robots_flags):
    idleness += 1
    for i, pos in enumerate(robots_positions):
        if robots_flags[i] == True:
            idleness[pos] = 0
    return idleness

# 记录每个点的idleness
idleness_history = np.zeros((n_points, time_steps))

# 模拟
for t in range(time_steps):
    robots_positions, random_mode, random_mode_steps, robots_remaining_steps, next_positions, robots_flags = update_positions(
        robots_positions, random_mode, random_mode_steps, robots_remaining_steps, next_positions, robots_speeds)
    idleness = update_idleness(idleness, robots_positions, robots_flags)
    idleness_history[:, t] = idleness

# 绘图函数
def plot_idleness(point, idleness_history):
    plt.figure()
    plt.plot(idleness_history[point])
    plt.title(f'Point {point} Idleness Over Time')
    plt.xlabel('Time Steps')
    plt.ylabel('Idleness')
    plt.show()

def plot_max_idleness(idleness_history):
    max_idleness = np.max(idleness_history, axis=0)
    plt.figure()
    plt.plot(max_idleness)
    plt.title('Maximum Idleness Over Time')
    plt.xlabel('Time Steps')
    plt.ylabel('Maximum Idleness')
    plt.show()

# 测试绘图函数
plot_idleness(0, idleness_history)
