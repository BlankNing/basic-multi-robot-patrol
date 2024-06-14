'''

challenge the capability(report anomaly, speed), predictability(choose to cooperate or not, stop probability), integrity(cooperate situation)

Robots patrol in museum(map) environment,
central monitor maintains the performance record todo: failure and success
Each in charge of 4 nodes,
stop with a probability of 0.05,
report true anomaly with probability of 0.95, false anomaly 0.05
notice closest robot, todo
choose to cooperate with probability 0.7 todo
'''

from patrol_class.EnvClass import BasicEnv as Env
from configs.basic_patrol_config import basic_patrol_config

config = basic_patrol_config

# prepare environment, robot, algo, trust model
env = Env(config)

# start simulation
for t in range(config['total_steps']):
    if t % 100 ==0:
        print(f"{t}/{config['total_steps']}")
    env.step()

# plot idleness, confusion matrix, reward
env.monitor.plot_idleness(0)
env.monitor.create_patrol_screenshot(config, 200)
env.monitor.create_patrol_gif(config)