# README

This is a basic multi-robot patrol simulator based on time-step simulation.

Robots can patrol in a given map and some interest points/nodes.

## Introduction

There are several elements in multi-robot patrol: environment, robots, algorithms and monitor.
Correspondingly, we have these four classes. 
+ The environment class is in charge of the whole simulation
by providing a method step().
+ The robot class is in charge of robot movement. 
+ The algor class is in charge  of path planning after a robot has reaches one node. 
+ The monitor class is in charge of recording metrics
and plot graphs and gifs.+
+ Besides we have Node class which records its idleness overtime, and this data is 
collected by monitor.

In main.py, we load config file from configs folder and BasicEnv class. Then use a simple loop
and env.step(), we can start the experiment

Entering into BasicEnv, we initialize Nodes, Robot, AlgorEngine and Monitor instances.

In env.step, node.step() first to increase idleness, then robot.step() to move its location.

## Usage

set up basic_patrol_config.py under ./configs to configure the experiment.

## Develop New Environment

### Develop New Robot

Some times we need to study heterogeneous robots, dynamic map and so on. We recommend you to write
new class under ./patrol_class folder inherit from the basic Robot, Env, Node.

### Develop New Patrol Algorithms

1. write new algorithm class under ./algo folder, inherit Algo.

2. set up algo_config_dispatch, describe what's needed in algo_config

3. set up this algo in AlgoFactory.

