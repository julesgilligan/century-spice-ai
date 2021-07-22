"""
Option 1: https://www.analyticsvidhya.com/blog/2019/04/introduction-deep-q-learning-python/
Option 2: https://towardsdatascience.com/reinforcement-learning-w-keras-openai-dqns-1eed3a5338c

"""
"""
Copied from https://towardsdatascience.com/why-going-from-implementing-q-learning-to-deep-q-learning-can-be-difficult-36e7ea1648af
as a starter Deep Q-Learning set up.

Try this one https://www.analyticsvidhya.com/blog/2019/04/introduction-deep-q-learning-python/
or the first one https://towardsdatascience.com/deep-q-learning-tutorial-mindqn-2a4c855abffc
skewed sampling or guided learning https://medium.com/@m.k.daaboul/dealing-with-sparse-reward-environments-38c0489c844d
shorter keras model https://towardsdatascience.com/reinforcement-learning-w-keras-openai-dqns-1eed3a5338c
"""


import numpy as np
import gym

from tensorflow import keras
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Activation, Flatten

from rl.agents.dqn import DQNAgent
from rl.policy import EpsGreedyQPolicy
from rl.memory import SequentialMemory

ENV_NAME = 'MountainCar-v0'


# Get the environment and extract the number of actions available in the Cartpole problem
env = gym.make(ENV_NAME)
np.random.seed(123)
env.seed(123)
# from .custom_dqn import CenturyEnv
# env = CenturyEnv()

nb_actions = env.action_space.n




state_shape  = env.observation_space.shape
print("HERE:", state_shape[0])
model   = Sequential()
model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
model.add(Dense(24, activation="relu"))
model.add(Dense(48, activation="relu"))
model.add(Dense(24, activation="relu"))
model.add(Dense(env.action_space.n))


print(model.summary())

policy = EpsGreedyQPolicy()
memory = SequentialMemory(limit=50000, window_length=1)
dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=10,
target_model_update=1, policy=policy)
dqn.compile(keras.optimizers.Adam(lr=5e-3), metrics=['mae'])


dqn.fit(env, nb_steps=5000)

dqn.test(env, nb_episodes=5, visualize=True)
