from dataclasses import dataclass, field
from enum import Enum

from termcolor import colored

from .switch import Caravan
from .structures import MerchantCard, PointCard


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
        self.score = 0
        if prev is None and a is None:
            self.len = 0
        elif prev is None:
            self.len = 1
        else:
            self.len = len(prev) + 1
            self.score += prev.score

        if a is not None and a.type == ActionType.SCORE:
            self.score += a.card['worth']
    
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
    goal: Caravan = field(compare = False)
    path: Path = field(compare = False, repr = False)
    hand: list[MerchantCard] = field(compare = False, repr = False)
    pcs: list[PointCard] = field(compare = False, repr = False)

    def __str__(self):
        return f"{self.priority}, {self.goal}, {self.path}"
    
    def __post_init__(self):
        # assumes Caravan is already self.goal no conversion needed
        if not isinstance(self.goal, Caravan):
            object.__setattr__(self, 'goal', Caravan(self.goal))

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
    
    def drop_last(self):
        object.__setattr__(self, 'path', self.path.prev)
        if self.path == None:
            object.__setattr__(self, 'path', Path())

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
    
