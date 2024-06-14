import time
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os

# params

point_num = 9 # desired number of interest points + 1
image_name = 'museum_test'
save_path = f'./results/{image_name}'
node_npy_name = f'{image_name}_node_positions.npy'
adj_npy_name = f'{image_name}_adj_matrix.npy'
map_image = np.array(Image.open(f"./{image_name}.pgm"))
print(map_image.shape)

if not os.path.exists(save_path):
    os.makedirs(save_path)
    print(f"{save_path} created")
else:
    print(f"{save_path} exisited")

def plot_final(pts, adjacency_matrix):
    plt.figure()
    plt.imshow(map_image)
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

# todo: regulate points
def regulate_points(pts):
    pts = pts[0:point_num-1]
    for i in range(len(pts)):
        pts[i] = np.round(pts[i]).astype(int)

    for i in range(len(pts)):
        for j in range(i+1, len(pts)):
            if abs(pts[i][0] - pts[j][0]) <= 20:
                pts[j][0] = pts[i][0]
            if abs(pts[i][1] - pts[j][1]) <= 20:
                pts[j][1] = pts[i][1]
    return pts

def tellme(s):
    print(s)
    plt.title(s, fontsize=16)
    plt.draw()

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

if __name__ == '__main__':

    plt.figure()
    plt.imshow(map_image)
    plt.xlim(0, map_image.shape[1])
    plt.ylim(0, map_image.shape[0])
    plt.gca().invert_yaxis()

    tellme('You will define interest points, click to begin')

    plt.waitforbuttonpress()

    while True:
        pts = []
        while len(pts) < point_num:
            tellme(f'Step 1: Select {point_num - 1} corners with mouse')
            pts = np.asarray(plt.ginput(point_num, timeout=-1, show_clicks=True))
            if len(pts) < point_num:
                tellme('Too few points, starting over')
                time.sleep(1)  # Wait a second
                continue

        print(f'Step2: Adjust Point Positions\nSize of the whole image:{map_image.shape[1],map_image.shape[0]}')
        pts = regulate_points(pts)

        for i, pt in enumerate(list(pts)):
            print(f'Point {i}: {pt}')

        plot_points(pts)
        a = input('Would you like to modify the position of these points?(y/n)\n')
        if a.lower() == 'y' or a.lower() == 'yes':
            while True:
                id = int(input('Which point would you like to modify:'))
                new_coordinate = input(f'The original coordinate is {pts[id]}, Please input the new coordinate and seperate x,y with space:')
                new_x = int(new_coordinate.split(' ')[0])
                new_y = int(new_coordinate.split(' ')[1])
                pts[id] = np.array([new_x, new_y])

                ans = input(f'New coordinate for Point {id} is set to {pts[id]} Would you like to continue? (y/n)\n')
                if ans == 'no' or 'n' or 'N':
                    break


        print('Step3: Determine connectivity\n This is your final point, please denote the connectivity between two nodes:')
        plot_points(pts)
        adjacency_matrix = np.zeros((point_num-1, point_num-1))

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

        for i in range(point_num - 1):
            print(f'Point {i}',adjacency_matrix[i])

        plot_final(pts,adjacency_matrix)
        adj_ans = input('This is your final adjacency matrix and your final map, would you like to change?(y/n)')
        if adj_ans.lower() =='y':
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
            Image.fromarray(map_image).save(f'{save_path}/{image_name}.pgm')
            print('Map image saved')
            break




