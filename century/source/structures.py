"""
Class structures and helpers for the AI.

Node, MerchantCard, PointCard, Path, Action, etc.
"""

import copy
from dataclasses import dataclass, field
from enum import Enum

from termcolor import colored

CUBE_STRING = [chr(11157)+" ",
        colored("  ", on_color='on_yellow'),
        colored("  ", on_color='on_red'),
        colored("  ", on_color='on_green'),
        colored("  ", on_color='on_magenta'),
        "5"]
COMPLENG_M = 9
COMPLENG_P = 5

@dataclass(frozen = True)
class PointCard():
    worth: int
    cost: list

    def __str__(self):
        out = colored(f"<|{self.worth}, ",'yellow')
        out += stringify_cubes(self.cost)
        out += colored("|>", 'yellow')
        return out
    
    def get(self, string):
        "String can be 'worth' or 'cost'. Use []"
        if string == 'worth':
            return self.worth
        if string == 'cost':
            return self.cost
        return None
    
    def __getitem__(self, key):
        return self.get(key)

    def __lt__(self, other):
        if self.worth != other.worth:
            return self.worth < other.worth
        if len(self.cost) != len(other.cost):
            return len(self.cost) < len(other.cost)
        if sum(self.cost) != sum(other.cost):
            return sum(self.cost) < sum(other.cost)
        return False

    def num_str(self):
        return str(self.worth) + "\t" + ' '.join(map(str, self.cost))
    
    def compress(self):
        """Length 5: 1 worth, 4 cost"""
        string = str(hex(self['worth']-6).split('x')[-1])
        string+= str(self['cost'].count(1)) + str(self['cost'].count(2))
        string+= str(self['cost'].count(3)) + str(self['cost'].count(4))
        if len(string) != COMPLENG_P:
            print(self)
            raise ValueError(f"PointCard compressed length {len(string)} isn't {COMPLENG_P}")
        return string

class MerchantCard():
    """
    Reprentation of merchant cards that trade cost list of spices for reward list, one direction.
    """
    def __init__(self, cost, reward):
        if isinstance(cost, list) and isinstance(reward, list):
            self.cost = cost
            self.reward = reward
            self.playable = True
        else:
            raise ValueError(f"Cost {cost} and Reward {reward} have to be lists.")
    
    def get(self, string):
        'String can be one of cost, reward, or playable. Use []'
        if string == 'cost':
            return self.cost
        if string == 'reward':
            return self.reward
        if string == 'playable':
            return self.playable    
        return None
    
    def copy(self):
        'Shallow copy using copy.copy()'
        return copy.copy(self)
    
    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, newvalue):
        if key == 'cost':
            self.cost = newvalue
        elif key == 'reward':
            self.reward = newvalue
        elif key == 'playable':
            self.playable = newvalue
        else:
            raise ValueError(f"Not accepted key: {key} with value {newvalue}")

    def __str__(self):
        cost = stringify_cubes(self['cost'])
        reward = stringify_cubes(self['reward'])
        return f"{cost}{CUBE_STRING[0]}{reward}"
    
    def __eq__(self, other):
        if isinstance(other, MerchantCard):
            return (self.cost == other.cost and self.reward == other.reward)
        return False

    def __lt__(self, other):
        if len(self.cost) != len(other.cost):
            return len(self.cost) < len(other.cost)
        if sum(self.cost) != sum(other.cost):
            return sum(self.cost) < sum(other.cost)
        if len(self.reward) != len(other.reward):
            return len(self.reward) < len(other.reward)
        if sum(self.reward) != sum(other.reward):
            return sum(self.reward) < sum(other.reward)
        return False

    def is_upgrade(self):
        # Any -> 5*times
        return 5 in self.reward
    
    def num_str(self):
        return  ' '.join(map(str, self['cost'])) + '->' + ' '.join(map(str, self['reward']))
    
    def compress(self):
        """Length 9: 4 cost, 4 reward, 1 playable"""
        string = str(self['cost'].count(1)) + str(self['cost'].count(2))
        string+= str(self['cost'].count(3)) + str(self['cost'].count(4))
        string+= str(self['reward'].count(1)) + str(self['reward'].count(2))
        string+= str(self['reward'].count(3)) + str(self['reward'].count(4))
        string+= '1' if self['playable'] else '0'
        if len(string) != COMPLENG_M:
            raise ValueError("MerchantCard compressed length isn't correct")
        return string

class ActionType(Enum):
    PLAY = 1
    BUY = 2
    SCORE = 3
    RECLAIM = 4

class Action():
    def __init__(self, t:ActionType, card = "All", plays = None):
        self.type: ActionType = t       
        self.card = card
        self.check_type_card()

        self.times = plays
        self.check_type_plays()

    def check_type_card(self):
        t = self.type
        card = self.card
        if t == ActionType.PLAY and not isinstance(card, MerchantCard): 
            raise TypeError("PLAY card isn't a MerchantCard")
        if t == ActionType.BUY and not isinstance(card, MerchantCard):
            raise TypeError("BUY card isn't a MerchantCard")
        if t == ActionType.SCORE and not isinstance(card, PointCard):
            raise TypeError("SCORE card isn't a PointCard")
        if t == ActionType.RECLAIM and card != "All":
            raise TypeError("RECLAIM doesn't accept a card")        

    def check_type_plays(self):
        t = self.type
        plays = self.times
        if plays != None and t != ActionType.PLAY:
            raise TypeError("Keyword 'plays' is for PLAY actions only")
        if t == ActionType.PLAY and (not isinstance(plays, int) or plays < 1):
            raise TypeError("Action 'plays' must be a positive int")
        
class Path():
    """Linked list of the path so far, pointing backward"""
    def __init__(self, a: Action = None, prev = None):
        self.head = a
        self.prev: Path = prev
        if prev is None and a is None:
            self.len = 0
        elif prev is None:
            self.len = 1
        else:
            self.len = len(prev) + 1
    
    def __iter__(self):
        if self.len > 0:
            self.it = None
        return self

    def __next__(self):
        try:
            if self.prev == self.it:
                del self.it
                return self.head
            temp = self.prev
            while temp.prev != self.it:
                temp = temp.prev
            self.it = temp
            return temp.head
        except AttributeError:
            raise StopIteration

    def __str__(self):
        string = ">Start>\n"
        for action in self:
            if action == None:
                string += "None\n"
                continue
            if action.type == ActionType.PLAY:
                if action.card.is_upgrade():
                    times = " U "
                else:
                    times = f"{action.times:^3}"
                string += f" {action.type.name:<4}{times} | {action.card.num_str()}\n"
            elif action.type in [ActionType.SCORE, ActionType.BUY]:
                string += f" {action.type.name:<7} | {action.card.num_str()}\n"
            else:
                string += f" {action.type.name:<7} | {action.card}\n"
        string += "<Get Goal<"
        return string

    def __colored_str__(self):
        string = colored(">Start>\n", 'blue', None, ['bold'])
        action: Action
        for action in self:
            if action.type == ActionType.PLAY:
                if action.card.is_upgrade():
                    times = " U "
                else:
                    times = f"{action.times:^3}"
                string += f" {action.type.name:<4}{times} | {action.card}\n"
            else:
                string += f" {action.type.name:<7} | {action.card}\n"
        string += colored("<Get Goal<\n", 'blue', None, ['bold'])
        return string

    def add(self, action: Action):
        if self.head is None:
            return Path(action)
        return Path(action, self)
    
    def __len__(self):
        'Number of actions in the path'
        return self.len
    
    def last_action(self):
        if self.head is None:
            return Action(ActionType.RECLAIM)
        return self.head

    def score(self):
        val = 0
        for a in self:
            if a.type == ActionType.SCORE:
                val += a.card.worth
        return val
    
    def already_scored(self, card:PointCard):
        return any((a.card == card for a in self))
    
    def set_front(self, a: Action):
        temp = self
        while temp.prev is not None:
            temp.len += 1
            temp = temp.prev
        temp.len += 1
        temp.prev = Path(a)
    
    def score_turn(self):
        turns = []
        for i, a in enumerate(self, 1):
            if a.type == ActionType.SCORE:
                turns.append(i)
        return turns

@dataclass(frozen = True, order = True)
class Node():
    priority: float = field(init=False)
    goal: list[int]
    path: Path = field(compare = False, repr = False)
    hand: list[MerchantCard] = field(compare = False, repr = False)
    pcs: list[PointCard] = field(compare = False, repr = False)

    def __str__(self):
        return f"{self.priority}, {self.goal}, {self.path}"
    
    def __post_init__(self):
        object.__setattr__(self, 'priority', len(self.path) + self.heuristic())

    def new_with(self, path: Path, caravan = None, hand = None, pcs = None):
        if caravan == None:
            caravan = self.goal.copy()
        if hand == None:
            hand = [x.copy() for x in self.hand]
        if pcs == None:
            pcs = self.pcs
        return Node(caravan, path, hand, pcs)
    
    def heuristic(self):
        '''A* heuristic for determining priority.'''
        play_bad = sum(1 for c in self.hand if not c['playable'])
        return 0 * play_bad

class NodeMutable(Node):
    def new_with(self, path: Path, caravan = None, hand = None, pcs = None):
        if caravan != None:
            object.__setattr__(self, 'goal', caravan)
        if hand != None:
            object.__setattr__(self, 'hand', hand)
        if pcs != None:
            object.__setattr__(self, 'pcs', pcs)
        object.__setattr__(self, 'path', self.path.add(path.head) )
        return self
    
    def drop_last(self):
        object.__setattr__(self, 'path', self.path.prev)
        if self.path == None:
            object.__setattr__(self, 'path', Path())

@dataclass
class GameState():
    merchant_list: list[MerchantCard]
    point_list: list[PointCard]
    silver: int = 8
    gold: int = 8

    def compress(self):
        """Length 79:\n
        6 Merchant Cards, 9 length each (0-53)\n
        5 Point Cards, 5 length each (54-78)"""
        string = ''.join(mc.compress() for mc in self.merchant_list)
        if len(self.merchant_list) < 6:
            string += (6 - len(self.merchant_list))*COMPLENG_M*'0'
        string += ''.join(pc.compress() for pc in self.point_list)
        if len(self.point_list) < 5:
            string += (5 - len(self.point_list))*COMPLENG_P*'0'
        if len(string) != (COMPLENG_M*6 + COMPLENG_P*5):
            raise ValueError(f"GameState compression is {len(string)} not expected {(COMPLENG_M*6 + COMPLENG_P*5)}")
        return string

@dataclass
class Player():
    caravan: list[int]
    hand: list[MerchantCard]
    score: int = 0
    point_count: int = 0

    def compress(self, hand_size = 4):
        """Length default 40: 4 caravan + 9*hand_size (0-39)"""
        string = str(hex(self.caravan.count(1)).split('x')[-1])
        string+= str(hex(self.caravan.count(2)).split('x')[-1])
        string+= str(hex(self.caravan.count(3)).split('x')[-1])
        string+= str(hex(self.caravan.count(4)).split('x')[-1])
        string+= ''.join(mc.compress() for mc in self.hand[:hand_size])
        if len(self.hand) < hand_size:
            string+= (hand_size - len(self.hand))*COMPLENG_M*'0'
        return string
    
    @staticmethod
    def starting_hand():
        return [MerchantCard([],[5,5]), MerchantCard([],[1,1])]

def str_hand(hand):
    return "| " + " | ".join(map(str, hand)) + " |"

def MCs_from_file(file):
    import numpy as np
    mc_list = []
    a = np.genfromtxt(file, dtype = str, delimiter='->', autostrip = True)
    for pair in a:
        cost = [int(x) for x in pair[0].split()]
        reward = [int(x) for x in pair[1].split()]
        mc_list.append(MerchantCard( sorted(cost) , sorted(reward)) )
    return mc_list

def PCs_from_file(file):
    import numpy as np
    lst = []
    a = np.genfromtxt(file, dtype = str, delimiter=',', autostrip = True)
    for item in a:
        worth = int(item[0])
        cost = [int(c) for c in item[1].split()]
        lst.append(PointCard( worth , sorted(cost) ))
    return lst

def stringify_cubes(spices):
    return ' '.join([CUBE_STRING[x] for x in spices])
