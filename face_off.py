import os
import random
from dataclasses import dataclass, field
from itertools import combinations_with_replacement
from typing import Callable

from century.classes import Path
from century.classes.cards import MerchantCard, PointCard
from century.classes.path import Action, ActionType
from century.core.SpiceAI import DFS, double_astar
from century.helpers.caravan_helpers import Caravan, append_each, remove_each
from century.helpers.helpers import MCs_from_file, PCs_from_file


@dataclass
class Agent():
    brain: Callable
    hand: list[MerchantCard] = field(default_factory = 
        lambda : [MerchantCard([],[1,1]), MerchantCard([],[5,5])]
        )
    caravan: Caravan = field(default_factory = 
        lambda : Caravan([1,1,1])
        ) 
    plan: Path = Path()
    vp: int = 0
    pc_cnt: int = 0

    def reclaim(self):
        for card in self.hand:
            card['playable'] = True

    def play(self, card, times):
        if card.is_upgrade():
            equiv_card = self.decypher_upgrade(card, times)
            for step in equiv_card:
                remove_each( self.caravan, step['cost'] )
                append_each( self.caravan, step['reward'] )
        else:
            remove_each( self.caravan, card['cost'] * times )
            append_each( self.caravan, card['reward'] * times )
        i = self.hand.index(card)
        self.hand[i]['playable'] = False

    def buy(self, card, count):
        remove_each( self.caravan, [1] * count )
        card['playable'] = True
        self.hand.append(card)

    def score(self, card):
        self.vp += card['worth']
        self.pc_cnt += 1

    def follow(self):
        if self.plan.prev == None:
            self.plan = Path()
        else:
            temp = self.plan
            while temp.prev.prev != None:
                temp = temp.prev
            temp.prev = None

    def next_action(self, face_ups):
        if len(self.plan) == 0:
            self.replan(face_ups)
        for action in self.plan:
            return action
        raise RuntimeError("plan length is still 0")
    
    def replan(self, face_ups):
        self.plan = self.brain(face_ups[0], self.hand, self.caravan, face_ups[1])

    def is_winner(self):
        return self.pc_cnt == 5
    
    def decypher_upgrade(self, upgrade, index):
        cnt = upgrade['reward'].count(5)
        effective_cards = [MerchantCard([1],[2]), MerchantCard([2],[3]), MerchantCard([3],[4])]

        def play_once(c):
            # 'caravan' comes from play_upgrade scope
            if car_cpy.count( c['cost'][0] ) > 0:
                remove_each(car_cpy, [ c['cost'][0] ] )
                append_each(car_cpy, [ c['reward'][0] ] )
                # car_cpy.sort()
                return True
            return False

        scan = 1
        for num in range(cnt):
            for comb in combinations_with_replacement(effective_cards, num + 1):
                car_cpy = self.caravan.copy()
                if all( map(play_once, comb) ):
                    if scan == index:
                        return comb
                    scan += 1

@dataclass
class Environment():
    mc_deck: list[MerchantCard]
    pc_deck: list[PointCard]

    def buy(self, card):
        i = self.mc_deck[:6].index(card)
        self.mc_deck.pop(i)
        return i

    def score(self, card):
        i = self.pc_deck[:5].index(card)
        self.pc_deck.pop(i)

    def face_ups(self):
        'first 5 point cards and first 6 merchant cards'
        assert len(self.pc_deck) >= 5
        assert len(self.mc_deck) >= 6
        return self.pc_deck[:5], self.mc_deck[:6]

def take_action(action: Action, table: Environment, player: Agent):
    if action.type == ActionType.RECLAIM:
        player.reclaim()
    elif action.type == ActionType.PLAY:
        player.play(action.card, action.times)
    elif action.type == ActionType.BUY:
        cnt = table.buy(action.card)
        player.buy(action.card, cnt)
    elif action.type == ActionType.SCORE:
        table.score(action.card)
        player.score(action.card)
    else:
        raise RuntimeError("action provided wasn't of any type")

    player.follow()

def isrecalc(action: Action):
    return action.type == ActionType.BUY or action.type == ActionType.SCORE

def main():
    # set up empty game
    curr_dir = os.path.dirname(__file__)
    with open(os.path.join(curr_dir, 'century/resources/MerchantCards.txt')) as f:
        mc_deck = MCs_from_file(f)[2:]
        random.shuffle(mc_deck)
    with open(os.path.join(curr_dir, 'century/resources/PointCards.txt')) as f:
        pc_deck = PCs_from_file(f)
        random.shuffle(pc_deck)
    
    table: Environment = Environment(mc_deck,  pc_deck)

    # create agents with double_astar and DFS
    agent1 = Agent(double_astar)
    agent2 = Agent(DFS)

    # environment loop taking actions from each
    while True:
        action = agent1.next_action(table.face_ups())
        take_action(action, table, agent1)
        
        # if isrecalc(action):
            # agent2.replan(table.face_ups())
        
        action = agent2.next_action(table.face_ups())
        take_action(action, table, agent2)
        
        if isrecalc(action):
            agent1.replan(table.face_ups())

        if agent1.is_winner() or agent2.is_winner():
            break

    # report result
    print("Agent 1 double_astar:", agent1.vp)
    print("Agent 2 DFS:", agent2.vp)

if __name__ == '__main__':
    main()
