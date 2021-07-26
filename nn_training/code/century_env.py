from typing import Counter
from code.package.structures import MerchantCard
import gym
from gym import Env, spaces

from .package import GameState, Player, MCs_from_file, PCs_from_file
import os
import random
from . import random_game, random_upgrade
import numpy as np


class CenturyEnv(Env):
    metadata = {'render.modes' : ['human']}
    action_meanings = {
            0: ["Play", 1],
            1: ["Play", 2],
            2: ["Play", 3],
            3: ["Play", 4],
            4: ["Play", 5],
            5: ["Play", 6],
            6: ["Buy", 1],
            7: ["Buy", 2],
            8: ["Buy", 3],
            9: ["Buy", 4],
            10: ["Buy", 5],
            11: ["Buy", 6],
            12: ["Reclaim", 6],
            13: ["Score", 1],
            14: ["Score", 2],
            15: ["Score", 3],
            16: ["Score", 4],
            17: ["Score", 5]
            }

    def __init__(self, start_hand_size = 4):
        super().__init__()
        
        # Currently a 1D observation vector from strucutres.*.compress() 
        self.observation_space = spaces.Box(low = np.zeros(137),
                                            high=np.ones(137) * 14, # write an accurate high?
                                            dtype = np.uint8)

        # Discrete action space (6 Plays + 6 Buys + 1 Reclaim + 5 Scores)
        self.action_space = spaces.Discrete(18)

        # Allow max_hand limits
        self.max_hand = 6
        assert 2 <= start_hand_size <= self.max_hand, f"Start hand size {start_hand_size} is invalid"
        self.start_hand_size = start_hand_size

        # Make a random game and player
        curr_dir = os.path.dirname(__file__)
        with open(os.path.join(curr_dir, 'package/MerchantCards.txt')) as f:
            MCs_Full = MCs_from_file(f)
        with open(os.path.join(curr_dir, 'package/PointCards.txt')) as f:
            PCs_Full = PCs_from_file(f)
        gs, p = random_game(MCs_Full[3:], PCs_Full, start_hand_size)

        # Match player caravan to a random point card so a single action can win
        p.caravan = random.choice( gs.point_list )['cost'].copy()
        
        # Collect remaining variables
        self.mc_deck = MCs_Full
        self.pc_deck = PCs_Full
        self.gs: GameState = gs
        self.player: Player = p
    
    def reset(self):
        # Make a random game and player
        curr_dir = os.path.dirname(__file__)
        with open(os.path.join(curr_dir, 'package/MerchantCards.txt')) as f:
            MCs_Full = MCs_from_file(f)
        with open(os.path.join(curr_dir, 'package/PointCards.txt')) as f:
            PCs_Full = PCs_from_file(f)
        gs, p = random_game(MCs_Full[3:], PCs_Full, self.start_hand_size)

        # Match player caravan to a random point card so a single action can win
        p.caravan = random.choice( gs.point_list )['cost'].copy()
        
        self.gs = gs
        self.player = p

        return self.state()

    def step(self, action) -> int:
        assert self.action_space.contains(action), f"Invalid Action {action}"
        
        # Delegate actions by value
        if (0 <= action <= 5):
            reward = self._play_card(action)
        elif (6 <= action <= 11):
            reward = self._buy_card(action-6)
        elif action == 12:
            reward = self._reclaim()
        elif (13 <= action <= 17):
            reward = self._score_card(action-13)
        else:
            raise ValueError(f"Action-space includes {action} but isn't handled")
        return self.state(), reward, self._is_winner(), {}
    
    def render(self, mode = 'human'):
        # obviously should actually printy pretty later 
        if mode == 'human':
            curr = self.state()
            # print("Merchant Cards")
            # for i in range(6):
            #     print(curr[0 + i*9:9 + i*9], end=" || ")
            
            print("> Point Cards")
            print("> ", end="")
            for i in range(5):
                print(curr[54 + i*5:59 + i*5], end=" || ")
            print()
            
            print("> Player")
            print(">", curr[79:83])
            print("> ", end="")
            for i in range(6):
                print(curr[83 + i*9:92 + i*9], end=" || ")
            print()
        else:
            super().render(mode=mode)

    def state(self):
        state: str = self.gs.compress()
        state += self.player.compress(self.max_hand)
        vec = np.array([int(x, 16) for x in state], dtype=int)
        if np.shape(vec) != self.observation_space.shape:
            raise ValueError(f"state is {np.shape(vec)} not {self.observation_space.shape} length")
        return vec
    
    ###
    # PRIVATE
    ###
    def _action_mask(self):
        """One-hot mask for which actions are allowable based on the current state"""
        mask = []
        caravan = Counter(self.player.caravan)
        for i in range(6):
            if i >= len(self.player.hand):
                mask.append(0)
                continue
            card = self.player.hand[i]
            if card['playable'] and 0 == sum(Counter(card['cost']) - caravan):
                mask.append(1)
            else:
                mask.append(0)
        
        for i in range(6):
            if len(self.player.hand) == self.max_hand:
                mask.append(0)
            elif i <= caravan[1]:
                mask.append(1)
            else:
                mask.append(0)
        
        if any(map(lambda c: not c['playable'], self.player.hand) ):
            mask.append(1)
        else:
            mask.append(0)

        for card in self.gs.point_list:
            if 0 == sum(Counter(card['cost']) - caravan):
                mask.append(1)
            else:
                mask.append(0)
        
        assert len(mask) == self.action_space.n, f"Mask is the wrong shape {len(mask)}, {self.action_space.n}"

        return np.array(mask)



    def _is_winner(self):
        return self.player.point_count > 0

    def _play_card(self, num):
        if num >= len(self.player.hand):
            return 0
        card = self.player.hand[num]
        card['playable'] = False
        if card.is_upgrade():
            card = random_upgrade() # Bad to just pick a random upgrade
        try:
            for i in card['cost']:
                self.player.caravan.remove(i)
            for i in card['reward']:
                self.player.caravan.append(i)
            self.player.caravan.sort()
            if len(self.player.caravan) > 10:
                self.player.caravan = random.choices(self.player.caravan, k = 10) # randomly choose which ones to keep
        except Exception:
            pass
        return 0

    def _buy_card(self, num):
        try:
            for _ in range(num):
                self.player.caravan.pop(0)
            card = self.gs.merchant_list.pop(num)
            self.gs.merchant_list.append(random.choice(self.mc_deck)) # technically doesn't track existing MCs
            if len(self.player.hand) < self.max_hand:
                self.player.hand.append(card)
        except Exception:
            return 0
        return 0

    def _reclaim(self):
        for card in self.player.hand:
            card['playable'] = True
        return 0

    def _score_card(self, num):
        card = self.gs.point_list[num]
        try:
            caravan_copy = self.player.caravan.copy()
            for i in card['cost']:
                self.player.caravan.remove(i)
        except Exception:
            self.player.caravan = caravan_copy
            return 0
        card = self.gs.point_list.pop(num)
        self.player.point_count += 1
        self.player.score += card.worth
        self.gs.point_list.append(random.choice(self.pc_deck)) # technically doesn't track existing PCs
        return card.worth