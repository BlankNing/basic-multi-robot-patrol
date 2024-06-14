import abc

class Algo(abc.ABC):
    @abc.abstractmethod
    def calculate_next_path(self, robot_id, current_node):
        '''
        given robot number and current node position, determine which node to go next. return planned path

        cannot handle change path at middle of the journey.

        :param robot_id:
        :param current_node:
        :return:
        '''
        pass
