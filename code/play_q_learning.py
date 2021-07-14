
"""
Still need to:
- Translate an integer action into something the environment understands.
- Extract the features meant for a model from the state, which often contains other metadata.
- Implement additional logic for detecting and handling the beginnings and endings of episodes.
"""
from collections import namedtuple
import random

from numpy import mean

from deep_q_learning import *
from package import GameState, Player, MCs_from_file, PCs_from_file
import program
import pickle
import matplotlib.pyplot as plt

EPISODE_NUM = 100
MAX_STEPS_PER_EPISODE = 500
SHOW_EVERY = 1000
LEARNING_DISCOUNT = .99
HAND_SIZE = 6

with open('package/MerchantCards.txt') as f:
    MCs_Full = MCs_from_file(f)
with open('package/PointCards.txt') as f:
    PCs_Full = PCs_from_file(f)

Observation = namedtuple('Observation', ('state','reward'))

class Environment():
    """ [0-5] Play from hand
        [6-11] Buy from trades
        [12] Reclaim
        [13-17] Score from points """

    action_len = 18
    state_len = 137
    hand_size = HAND_SIZE

    def __init__(self, gamestate: GameState, player: Player):
        self.gs = gamestate
        self.p1 = player
    
    def state(self, player):
        state: str = self.gs.compress()
        if player == 'p1':
            state += self.p1.compress(Environment.hand_size)
        if len(state) != Environment.state_len:
            print("Error Start")
            print(len(self.p1.compress(Environment.hand_size)), 58)
            print(self.p1.caravan)
            print(self.p1.compress(Environment.hand_size))
            raise ValueError(f"state is {len(state)} not {Environment.state_len} length")
        return [int(x, 16) for x in state.split()]
    
    def do_action(self, action, player) -> int:
        if (0 <= action <= 5):
            return self._play_card(action, player)
        elif (6 <= action <= 11):
            return self._buy_card(action-6, player)
        elif action == 12:
            return self._reclaim('player')
        elif (13 <= action <= 17):
            return self._score_card(action-13, player)
        else:
            raise ValueError(f"Action number {action} out of bounds")

    def is_winner(self):
        return self.p1.point_count > 0

    def _play_card(self, num, player):
        if num >= len(self.p1.hand):
            return 0
        card = self.p1.hand[num]
        card['playable'] = False
        if card.is_upgrade():
            card = program.random_upgrade() # Bad to just pick a random upgrade
        try:
            for i in card['cost']:
                self.p1.caravan.remove(i)
            for i in card['reward']:
                self.p1.caravan.append(i)
            self.p1.caravan.sort()
            if len(self.p1.caravan) > 10:
                self.p1.caravan = random.choices(self.p1.caravan, k = 10) # randomly choose which ones to keep
        except:
            pass
        return 0

    def _buy_card(self, num, player):
        try:
            for _ in range(num):
                self.p1.caravan.pop(0)
            card = self.gs.merchant_list.pop(num)
            self.gs.merchant_list.append(random.choice(MCs_Full)) # technically doesn't track existing MCs
            if len(self.p1.hand) < Environment.hand_size:
                self.p1.hand.append(card)
        except:
            return 0
        return 0

    def _reclaim(self, player):
        for card in self.p1.hand:
            card['playable'] = True
        return 0

    def _score_card(self, num, player):
        card = self.gs.point_list[num]
        try:
            for i in card['cost']:
                self.p1.caravan.remove(i)
        except:
            return 0
        card = self.gs.point_list.pop(num)
        self.p1.point_count += 1
        self.p1.score += card.worth
        self.gs.point_list.append(random.choice(PCs_Full)) # technically doesn't track existing PCs
        return card.worth


p1: Agent = Agent(Environment.state_len, Environment.action_len, target_update_freq = 1, batch_size = 32,
    replay_memory_size = 100, replay_start_size = 32, discount = LEARNING_DISCOUNT)
# p2: Agent = Agent(STATE_LEN, ACTION_LEN, target_update_freq = 100, batch_size = 3,
# replay_memory_size = 200, replay_start_size = 200, discount = LEARNING_DISCOUNT)

episode_scores = []
for episode in range(EPISODE_NUM):
    gs, p = program.random_game(MCs_Full[3:], PCs_Full, 4)
    p.caravan = random.choice( gs.point_list )['cost'].copy()
    env = Environment(gs, p)

    p1.handle_episode_start()
    # p2.handle_episode_start()
    
    #
    # Start game
    #
    p1_last_state = env.state('p1')
    p1_last_reward = 0
    winner = False
    step_start = p1.steps
    ep_reward = 0
    while not winner:
        # Player 1 go
        observation = Observation(p1_last_state, p1_last_reward)
        
        action = p1.step(observation)

        p1_last_reward = env.do_action(action, 'p1')
        p1_last_state = env.state('p1')
        ep_reward += p1_last_reward
        winner = env.is_winner()
        if p1.steps - step_start >= MAX_STEPS_PER_EPISODE:
            break
        
    episode_scores.append( (ep_reward, p1.steps) )
    # if ep_reward > 0:
    #     print(f"episode {episode} got to ({ep_reward}, {p.score}) in {p1.steps - step_start} steps")  
    if episode % SHOW_EVERY == 0:
        print(f"episode {episode} got to ({ep_reward}, {p.score}) in {p1.steps - step_start} steps")
        
window_size = 32
moving_average = [ mean( list(map( lambda x: x[0], episode_scores[i-window_size:i] ))) for i in range(window_size, len(episode_scores))  ]
plt.plot([i for i in range(len(moving_average))], moving_average)
plt.show()

# with open("last_agent.pickle", 'wb') as f:
#     pickle.dump(p1, f)
