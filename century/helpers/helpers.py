import random
import re

from century.classes import GameState, MerchantCard, Player, PointCard


def read_point_card(card = None):
    ''' 'card' : a string to be parsed as a PointCard. 
    Asks at the command line if arg is missing. 
    Returns PointCard or None if parsing fails'''
    if card is None:
        card = input()
    card = re.split('\s|,', card, 1)
    try:
        value =  int(re.findall('(\d{2}|\d{1})', card[0])[0])
        reward = sorted([int(x) for x in re.findall('[1-4]{1}', card[1])])
        return PointCard(value, reward)
    except IndexError:
        return None

def read_merchant_card(card = None):
    ''' 'card' : a string to be parsed as a MerchantCard. 
    Asks at the command line if arg is missing. 
    Returns MerchantCard or None if parsing fails'''
    if card is None:
        card = input()
    card = re.split('->|,', card)
    try:
        fives = re.findall('5{1}', card[1])
        if fives:
            cost = []
            reward = max(min(len(fives), 3), 2) * [5]
        else:
            cost = [int(x) for x in re.findall('[1-4]{1}', card[0])][:5]
            reward = [int(x) for x in re.findall('[1-4]{1}', card[1])][:5]
        return MerchantCard(sorted(cost), sorted(reward))
    except IndexError:
        return None 

def random_caravan():
    lst =     [1]* random.choices( [1,2,3,4], weights = [10,30,40,20] )[0]
    lst.extend( [2]* random.choices( [0,1,2], weights = [50,40,10] )[0])
    lst.extend( [3]* random.choices( [0,1,2], weights = [80,15, 5] )[0])
    lst.extend( [4]* random.choices( [0,1,2], weights = [90, 8, 2] )[0])
    return lst

def random_game(select_mcs, select_pcs, hand_size):
    # Playing Random Games
    mList = random.sample(select_mcs, 6+hand_size-2)
    pList = random.sample(select_pcs, 5)
    gs = GameState(mList[:6], pList)
    hand = mList[6:]
    hand.append(MerchantCard([],[1,1]))
    hand.append(MerchantCard([],[5,5]))
    random.shuffle(hand)
    caravan = random_caravan()
    p = Player(caravan,hand)
    return gs, p

def random_upgrade():
    effective_cards = [MerchantCard([1],[2]), MerchantCard([2],[3]), MerchantCard([3],[4])]
    return random.choice(effective_cards)


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
