from load_map import *

map_name = 'museum'
patrol_algo = 'partition'
timesteps = 1000
robots_num = 8

basic_patrol_config = {
    'env_config':{
        'map_name': map_name,
        'node_pos_matrix':get_node_pos_matrix(map_name),
        'map_adj_matrix':get_map_adj_matrix(map_name),
        'pgm_map_matrix':get_pgm_map_matrix(map_name),
    },
    'robot_config':{
        'robots_num': robots_num,
        'init_pos': get_default_init_pos(get_node_pos_matrix(map_name),robots_num),
    },
    'algo_config':{
        'patrol_algo_name':patrol_algo,
    },
    'trust_config':{
        None
    },
    'total_steps':timesteps,
}
