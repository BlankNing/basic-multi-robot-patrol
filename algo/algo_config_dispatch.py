def get_algo_config(config_file):
    map_name = config_file['env_config']['map_name']
    node_pos_matrix = config_file['env_config']['node_pos_matrix']
    map_adj_matrix = config_file['env_config']['map_adj_matrix']
    pgm_map_matrix = config_file['env_config']['pgm_map_matrix']
    patrol_algo = config_file['algo_config']['patrol_algo_name']
    init_pos = config_file['robot_config']['init_pos']
    robots_num = config_file['robot_config']['robots_num']

    if patrol_algo == 'partition':
        partition_algo_config  = {
            'robots_num': robots_num,
            'nodes_num': len(node_pos_matrix),
            'pgm_map_matrix': pgm_map_matrix,
            'node_pos_matrix': node_pos_matrix
        }
        return partition_algo_config

    elif patrol_algo == 'SEBS':
        pass