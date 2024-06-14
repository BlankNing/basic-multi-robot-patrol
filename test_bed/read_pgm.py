import numpy as np
from PIL import Image
import heapq
from scipy.spatial.distance import euclidean as scipy_euclidean

# 读取PGM图像并将其转换为numpy数组
def read_pgm_image(file_path):
    with open(file_path, 'rb') as f:
        img = Image.open(f)
        img_array = np.array(img)
    return img_array

def astar(map_matrix, start, goal):
    """
    Implementation of A* path planning algorithm
    @param map_matrix: A 2D numpy array representing the map with obstacles. 0's represent obstacles and non-zero values represent empty cells.
    @param start: The starting position on the map, represented as a tuple of (x,y).
    @param goal: The goal position on the map, represented as a tuple of (x,y).
    @return: A list of coordinates representing the optimal path from the start to the goal, or False if no path is found.
    """
    map_matrix = np.transpose(map_matrix)
    neighbours = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    start = tuple(start)
    goal = tuple(goal)
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: scipy_euclidean(start, goal)}
    oheap = []
    heapq.heappush(oheap, (fscore[start], start))

    while oheap:
        current = heapq.heappop(oheap)[1]

        if current[0] == goal[0] and current[1] == goal[1]:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data[::-1]

        close_set.add(current)
        for i, j in neighbours:
            neighbour = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + scipy_euclidean(current, neighbour)
            if not 0 <= neighbour[0] < map_matrix.shape[0]:
                continue

            if not 0 <= neighbour[1] < map_matrix.shape[1]:
                continue
            if map_matrix[neighbour] == 0:  # Continue if the neighbour is an obstacle
                continue
            if neighbour in close_set and tentative_g_score >= gscore.get(neighbour, 0):
                continue

            if tentative_g_score < gscore.get(neighbour, 0) or neighbour not in [i[1] for i in oheap]:
                came_from[neighbour] = current
                gscore[neighbour] = tentative_g_score
                fscore[neighbour] = tentative_g_score + scipy_euclidean(neighbour, goal)
                heapq.heappush(oheap, (fscore[neighbour], neighbour))

    return False

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# 计算最短路径
def calculate_shortest_path(image_path, start, goal):
    img_array = read_pgm_image(image_path)
    path = astar(img_array, start, goal)
    if path:
        path = path[::-1]  # reverse the path to get it from start to goal
    return path

# 示例
image_path = '../maps/museum/museum.pgm'
start = (430 ,140)  # 起点坐标
goal = (430, 142)   # 终点坐标
path = calculate_shortest_path(image_path, start, goal)
print(path)
