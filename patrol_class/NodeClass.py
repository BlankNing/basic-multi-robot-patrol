class Node():
    def __init__(self, id, pos_info):
        self.id = id
        self.pos_info = tuple(pos_info)
        self.idleness = 0

    def step(self, robot_current_pos):
        if self.pos_info not in robot_current_pos:
            self.idleness += 1
        else:
            self.reset()
        return self.idleness

    def reset(self):
        self.idleness = 0
