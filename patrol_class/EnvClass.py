'''
Robot: update position according to patrol algorithm
Algo: return the next path for robot when it reaches a node
Node: record idleness
Monitor: write log, store node idleness, robot trajectory, robot probability info.
'''

from .RobotClass import Robot
from .NodeClass import Node
from .MonitorClass import Monitor
from .AlgoClass import AlgoFactory
from algo.algo_config_dispatch import get_algo_config


class Env:
    def __init__(self, map_name, node_pos_matrix, map_adj_matrix, pgm_map_matrix, patrol_algo, robots_num, init_pos, algo_config):
        # init nodes and map
        self.map_name = map_name
        self.node_pos_matrix = node_pos_matrix
        self.map_adj_matrix = map_adj_matrix
        self.pgm_map_matrix = pgm_map_matrix

        # init Robot, Node, Monitor
        self.nodes_num = len(self.map_adj_matrix[0])
        self.nodes = [Node(i, node_pos_matrix[i]) for i in range(self.nodes_num)]
        print("Nodes have been set up")
        self.algo_engine = AlgoFactory().create_algo(patrol_algo, algo_config)
        print("Algorithms have been set up")
        self.robots = [Robot(i, self.algo_engine, node_pos_matrix, init_pos[i]) for i in range(robots_num)]
        print("Robots have been set up")
        self.monitor = Monitor()
        print("Monitor is ready")

    def step(self,verbose=False):
        # robot move
        robot_pos_records = []
        for robot in self.robots:
            robot_pos_record = robot.step(verbose=verbose)
            robot_pos_records.append(robot_pos_record)
        self.monitor.collect_robot_pos(robot_pos_records)

        # node record
        node_idleness_records = []
        for node in self.nodes:
            node_idleness_record = node.step(robot_pos_records)
            node_idleness_records.append(node_idleness_record)
        self.monitor.collect_node_idleness(node_idleness_records)


class BasicEnv:
    def __init__(self, config_file):
        # load basic_patrol variables from config_file
        self.map_name = config_file['env_config']['map_name']
        self.node_pos_matrix = config_file['env_config']['node_pos_matrix']
        self.map_adj_matrix = config_file['env_config']['map_adj_matrix']
        self.pgm_map_matrix = config_file['env_config']['pgm_map_matrix']

        self.patrol_algo = config_file['algo_config']['patrol_algo_name']
        self.patrol_algo_config = get_algo_config(config_file)

        self.init_pos = config_file['robot_config']['init_pos']
        self.robots_num = config_file['robot_config']['robots_num']

        # init Robot, Node, Monitor
        self.nodes_num = len(self.map_adj_matrix[0])

        self.nodes = [Node(i, self.node_pos_matrix[i]) for i in range(self.nodes_num)]
        print("Nodes have been set up")
        self.algo_engine = AlgoFactory().create_algo(self.patrol_algo, self.patrol_algo_config)
        print("Algorithms have been set up")
        self.robots = [Robot(i, self.algo_engine, self.node_pos_matrix, self.init_pos[i]) for i in range(self.robots_num)]
        print("Robots have been set up")
        self.monitor = Monitor()
        print("Monitor is ready")


    def step(self,verbose=False):
        # robot move
        robot_pos_records = []
        for robot in self.robots:
            robot_pos_record = robot.step(verbose=verbose)
            robot_pos_records.append(robot_pos_record)
        self.monitor.collect_robot_pos(robot_pos_records)

        # node record
        node_idleness_records = []
        for node in self.nodes:
            node_idleness_record = node.step(robot_pos_records)
            node_idleness_records.append(node_idleness_record)
        self.monitor.collect_node_idleness(node_idleness_records)