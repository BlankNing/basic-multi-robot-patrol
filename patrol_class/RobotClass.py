import numpy as np

'''
step 0: judge path_list == empty
step 1: if empty, check current position
step 2: else 

'''
class Robot():
    def __init__(self, id, algo_engine, node_pos_matrix, init_pos):
        self.id = id
        self.algo_engine = algo_engine
        self.path_list = []
        self.last_node = -1
        self.current_pos = init_pos
        self.node_pos_matrix = node_pos_matrix
        self.state = 'Patrolling'

    def check_node(self):
        return np.where((self.node_pos_matrix == self.current_pos).all(axis=1))[0]

    def step(self,verbose = False):
        if self.path_list == []:
            self.last_node = int(self.check_node())
            self.path_list = self.algo_engine.calculate_next_path(self.id, self.last_node)

        # move 1 step
        self.current_pos = self.path_list[0]
        self.path_list.pop(0)

        if verbose == True:
            print(f"Robot_{self.id} {self.state} at {self.current_pos} {self.last_node}")

        return self.current_pos