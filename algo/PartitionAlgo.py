from patrol_class.AbstractAlgo import Algo
from .astar_shortest_path import calculate_shortest_path

class PartitionAlgo(Algo):
    def __init__(self, algo_config):
        self.nodes_num = algo_config['nodes_num']
        self.robots_num = algo_config['robots_num']
        self.pgm_map_matrix = algo_config['pgm_map_matrix']
        self.node_pos_matrix = algo_config['node_pos_matrix']

    def determine_goal(self, robot_id, current_node):
        charge_num = self.nodes_num/self.robots_num
        goal_node = int((current_node + 1) % charge_num + robot_id * charge_num)
        return self.node_pos_matrix[goal_node]

    def calculate_next_path(self, robot_id, current_node):
        start = self.node_pos_matrix[current_node]
        goal = self.determine_goal(robot_id, current_node)
        return calculate_shortest_path(self.pgm_map_matrix, start, goal)

