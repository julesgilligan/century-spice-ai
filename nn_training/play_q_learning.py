import gym
import random
import os
import numpy as np
from collections      import deque
from keras.models     import Sequential
from keras.layers     import Dense
from keras.optimizers import Adam

from dqn_agent import Agent
debug_dict = {}
class CartPole:
    def __init__(self):
        self.sample_batch_size = 32
        self.episodes          = 500
        # self.env               = gym.make('CartPole-v1')
        self.env = gym.make('MountainCar-v0')
        
        self.state_size        = self.env.observation_space.shape[0]
        self.action_size       = self.env.action_space.n
        self.agent             = Agent(self.state_size, self.action_size)


    def run(self):
        try:
            for index_episode in range(self.episodes):
                state = self.env.reset()

                state = np.reshape(state, [1, self.state_size])

                done = False
                index = 0
                while not done:
                    action = self.agent.act(state)

                    next_state, reward, done, _ = self.env.step(action)
                    next_state = np.reshape(next_state, [1, self.state_size])
                    self.agent.remember(state, action, reward, next_state, done)
                    state = next_state
                    index += 1

                # print("Episode {}# Score: {}".format(index_episode, index))
                # debug_dict.setdefault('final_positions', []).append((index_episode, index))
                print("Episode {}# Score: {}".format(index_episode, next_state[0][0]))
                debug_dict.setdefault('final_positions', []).append((index_episode, next_state[0][0]))
                self.agent.replay(self.sample_batch_size, index_episode)
                if index_episode % 5 == 0:
                    self.agent.target_train()
        finally:
            import matplotlib.pyplot as plt
            roll_av = moving_average([i[1] for i in debug_dict['final_positions']])
            debug_dict.update( {'moving_average':
                [ (i, item)  for i, item in enumerate(roll_av, start=20) ]
            } )
            for key in debug_dict:
                xs = [x[0] for x in debug_dict[key]]
                ys = [y[1] for y in debug_dict[key]]
                plt.plot(xs, ys)
                plt.ylabel(key)
                plt.show()
            # plt.plot(np.arange(len(episode_scores)), episode_scores)
            
            # self.agent.save_model()

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

if __name__ == "__main__":
    cartpole = CartPole()
    cartpole.run()
