from .package import *
import random

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