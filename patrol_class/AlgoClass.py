from algo.PartitionAlgo import PartitionAlgo

class AlgoFactory():
    @staticmethod
    def create_algo(patrol_algo, algo_config):
        if patrol_algo == 'partition':
            return PartitionAlgo(algo_config)
