import gym
import random
import os
import numpy as np
from collections      import deque
from keras.models     import Sequential
from keras.layers     import Dense
from keras.optimizers import Adam

class Agent():
    def __init__(self, state_size, action_size):
        self.weight_backup      = "cartpole_weight.h5"
        self.state_size         = state_size
        self.action_size        = action_size
        self.memory             = deque(maxlen=2000)
        self.learning_rate      = 0.001
        self.gamma              = 0.95
        self.exploration_rate   = 1.0
        self.exploration_min    = 0.01
        # 99.5% = 140\920 to reach half\minimum
        # 99.3% = 100\655 to reach half\minimum
        # 99% = 70\460 to reach half\minimum
        self.exploration_decay  = 0.993

        self.brain              = self._build_model()
        self.target_network     = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))

        if os.path.isfile(self.weight_backup):
            model.load_weights(self.weight_backup)
            self.exploration_rate = self.exploration_min
        return model

    def save_model(self):
        self.brain.save(self.weight_backup)

    def act(self, state):
        if np.random.rand() <= self.exploration_rate:
            return random.randrange(self.action_size)
        act_values = self.brain.predict(state)
        return np.argmax(act_values[0])

    def remember(self, state, action, reward, next_state, done):
        # Only for MountainCar. This overrides the usual -1 every step
        reward = state[0][0] + 0.5
        if state[0][0] > 0.5:
            reward += 1
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, sample_batch_size, episode):
        if len(self.memory) < sample_batch_size:
            return
        sample_batch = np.array( random.sample(self.memory, sample_batch_size), dtype=object )

        states = np.squeeze(  np.stack(sample_batch[:,0]) )
        actions = np.stack(sample_batch[:,1])
        rewards = np.stack(sample_batch[:,2])
        next_states = np.squeeze( np.stack(sample_batch[:,3]) )
        dones = np.stack(sample_batch[:,4])

        ### Fast concurrent
        targets = self.target_network.predict(states)
        futures = np.amax( self.target_network.predict(next_states) , axis=1 )
        for i, done in enumerate(dones):
            if done:
                futures[i] = 0

        one_hots = np.eye(self.action_size)[actions]
        inverse = 1 - one_hots
        targets = inverse * targets
        targets += one_hots * (rewards + futures * self.gamma)[:,np.newaxis]
        self.brain.fit(states, targets, epochs=10, verbose =0)
        ### Fast concurrent
        

        if self.exploration_rate > self.exploration_min:
            self.exploration_rate *= self.exploration_decay

    def target_train(self):
        weights = self.brain.get_weights()
        # target_weights = self.target_model.get_weights()
        # # w/ np arrays: target = weights * self.tau + target * (1-self.tau)
        # for i in range(len(target_weights)):
        #     # example kinda doesn't use this
        #     target_weights[i] = weights[i]*self.tau + target_weights[i] * (1-self.tau)
        self.target_network.set_weights(weights)
