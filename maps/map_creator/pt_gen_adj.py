import time
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os

# params
point_num = 33
image_name = 'museum_regulate'
save_path = f'./map_creator/results/{image_name}'
node_npy_name = f'{image_name}_node_positions.npy'
adj_npy_name = f'{image_name}_adj_matrix.npy'
map_image = np.array(Image.open(f"./map_creator/{image_name}.png"))

# 检查路径是否存在
if not os.path.exists(save_path):
    # 如果路径不存在，则创建
    os.makedirs(save_path)
    print(f"{save_path} created")
else:
    print(f"{save_path} exisited")

#begin

def plot_final(pts, adjacency_matrix):
    plt.figure()
    plt.imshow(map_image)  # 将地图图像作为背景
    plt.xlim(0, map_image.shape[1])
    plt.ylim(0, map_image.shape[0])
    plt.gca().invert_yaxis()
    plt.title('Final Plot')
    plt.scatter(pts[:, 0], pts[:, 1], color='red', s=50)
    for i, pt in enumerate(pts):
        plt.text(pt[0], pt[1], f'{i}', fontsize=12, ha='center', va='center', color='white')
    for i in range(adjacency_matrix.shape[0]):
        for j in range(i + 1, adjacency_matrix.shape[1]):
            if adjacency_matrix[i, j] != 0:
                plt.plot([pts[i][0], pts[j][0]], [pts[i][1], pts[j][1]], 'b-')
    plt.savefig(f'{save_path}/{image_name}_final_plot.png')


def plot_points(pts):
    plt.figure()
    plt.imshow(map_image)
    plt.xlim(0, map_image.shape[1])
    plt.ylim(0, map_image.shape[0])
    plt.gca().invert_yaxis()
    plt.scatter(pts[:, 0], pts[:, 1], color='red', s=60)
    for i, pt in enumerate(pts):
        plt.text(pt[0], pt[1], f'{i}', fontsize=10, ha='center', va='center', color='white')
    plt.savefig(f'{save_path}/{image_name}_points_plot.png')

# todo: define your points positions
pts = np.array([
    [160,140],[160,50],[70,140],[250,140],[160,260],[160,350],[70,260],[250,260],
    [430,140],[430,50],[340,140],[520,140],[430,260],[430,350],[340,260],[520,260],
    [690,140],[690,50],[600,140],[780,140],[690,260],[690,350],[600,260],[780,260],
    [960,140],[960,50],[870,140],[1050,140],[960,260],[960,350],[870,260],[1050,260],
])

connection_file = True
current_dir = os.getcwd()
connection_file_path = f'{current_dir}/map_creator/connection_file.txt'

print('Step3: Determine connectivity\nThis is your final point, please denote the connectivity between two nodes:')
plot_points(pts)
adjacency_matrix = np.zeros((point_num - 1, point_num - 1))

if connection_file == False:
    # Iterate through each point and ask for its connections with other points
    for i in range(point_num - 1):
        print(f"Connectivity for point {i}:")
        connections = input(
            f"Enter the connected points separated by spaces (e.g., for connections with points greater than {i}, enter their indices): ").split()
        for conn in connections:
            j = int(conn)
            if j > i:  # Ensure symmetry
                weight = np.linalg.norm(pts[i] - pts[j])
                adjacency_matrix[i, j] = weight
                adjacency_matrix[j, i] = weight
else:
    print('Oh! you have a connection file!')
    with open(connection_file_path, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        connections = line.strip().split()
        for conn in connections:
            j = int(conn)
            if j > i:  # Ensure symmetry
                weight = np.linalg.norm(pts[i] - pts[j])
                adjacency_matrix[i, j] = weight
                adjacency_matrix[j, i] = weight

for i in range(point_num - 1):
    print(f'Point {i}', adjacency_matrix[i])

plot_final(pts, adjacency_matrix)
adj_ans = input('This is your final adjacency matrix and your final map, would you like to change?(y/n)')
if adj_ans.lower() == 'y':
    while True:
        adj_points = input('Which two points would you like to connect? seperate by space')
        i = int(adj_points.split(' ')[0])
        j = int(adj_points.split(' ')[1])
        weight = np.linalg.norm(pts[i] - pts[j])
        adjacency_matrix[i, j] = weight
        adjacency_matrix[j, i] = weight
        adjf_ans = input('Would you like to continue?(y/n)')
        if adjf_ans == 'n':
            break

f_ans = input('Are u happy?(y/n)')
if f_ans.lower() == 'y' or f_ans.lower() == 'yes':
    np.save(f'{save_path}/{node_npy_name}', pts)
    print('Node file saved')
    np.save(f'{save_path}/{adj_npy_name}', adjacency_matrix)
    print('Adjacent matrix saved')
    print('Final Plot Saved')

