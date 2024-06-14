# config.py

# Total number of nodes
TOTAL_NODES = 32

# Number of robots and their assignment of nodes
NUM_ROBOTS = 8
NODES_PER_ROBOT = TOTAL_NODES // NUM_ROBOTS

# Patrol periods
BASE_PATROL_PERIOD = 20
SLOW_PATROL_PERIOD = 60
SLOW_START = 400

# Simulation parameters
TIME_STEP = 1
TOTAL_TIME = 2000  # 1-second time step, 2000 seconds total

# Reassignment parameters
REASSIGNMENT_TIME = 700
REASSIGN_FROM_ROBOT = 0
REASSIGN_TO_ROBOT = 1
REASSIGN_NODE_ID = 3

# Trust Parameters
TRUST_THRESHOLD = 0.4