"""
tests for the various functions. Run 'pytest' in shell from the project directory
"""

from collections import Counter

import pytest

from package import ActionType, MerchantCard, PointCard

from .SpiceAI import DFS, forward_astar, pay_pcs, play_card, play_upgrade


def test_play_card():
    mmc = MerchantCard
    # Zero cost always true
    assert play_card(mmc([],[]), []) == [(1, [])]
    assert play_card(mmc([],[3]), []) == [(1,[3])]
    assert play_card(mmc([],[]), [2]) == [(1, [2])]
    assert play_card(mmc([],[3]), [2]) == [(1, [2,3])]
    # Simple cost true when payable
    assert play_card(mmc([1],[]), []) == False
    assert play_card(mmc([1],[]), [2]) == False
    assert play_card(mmc([1],[]), [1]) == [(1, [])]
    assert play_card(mmc([1],[]), [1,2]) == [(1, [2])]
    assert play_card(mmc([1],[3]), [1,2]) == [(1, [2,3])]
    # Complex cost has to be fully matched
    assert play_card(mmc([1,1,2],[]), [1,2]) == False
    assert play_card(mmc([1,1,2],[]), [1,1,3]) == False
    assert play_card(mmc([1,1,2],[1]), [1,1,3]) == False
    assert play_card(mmc([1,1,2],[1]), [1,1,2]) == [(1, [1])]
    # Cards can play once or twice if met
    assert play_card(mmc([1,2],[3]), [1,1,2]) == [(1, [1,3])]
    assert play_card(mmc([1,2],[3]), [1,1,2,2]) == [(1,[1,2,3]),(2,[3,3])]
    test_res = [1,1,1]
    assert play_card(mmc([1],[3]), test_res) == [(1,[1,1,3]),(2,[1,3,3]),(3,[3,3,3])]
    # shouldn't change because of function call
    assert test_res == [1,1,1]

def test_play_upgrades():
    uc2 = MerchantCard([],[5,5])
    # Single cube upgrades
    assert play_upgrade(uc2, []) == False
    assert play_upgrade(uc2, [1]) == [(1, [2]),(2, [3])]
    assert play_upgrade(uc2, [2]) == [(1, [3]),(2, [4])]
    assert play_upgrade(uc2, [3]) == [(1, [4])]
    assert play_upgrade(uc2, [4]) == False
    # Double cubes
    assert play_upgrade(uc2, [1,1]) == [(1, [1,2]),(2, [2,2]),(3, [1,3])]
    assert play_upgrade(uc2, [1,2]) == [(1, [2,2]),(2, [1,3]),(3, [2,3]),(4, [1,4])]
    assert play_upgrade(uc2, [1,3]) == [(1, [2,3]),(2, [1,4]),(3, [3,3]),(4, [2,4])]
    assert play_upgrade(uc2, [1,4]) == [(1, [2,4]),(2, [3,4])]
    assert play_upgrade(uc2, [2,2]) == [(1, [2,3]),(2, [3,3]),(3, [2,4])]
    assert play_upgrade(uc2, [2,3]) == [(1, [3,3]),(2, [2,4]),(3, [3,4])]
    assert play_upgrade(uc2, [2,4]) == [(1, [3,4]),(2, [4,4])]
    assert play_upgrade(uc2, [3,3]) == [(1, [3,4]),(2, [4,4])]
    assert play_upgrade(uc2, [3,4]) == [(1, [4,4])]
    assert play_upgrade(uc2, [4,4]) == False
    # On full resources
    test_res = [1,1,2,2,3,3,4,4]
    assert play_upgrade(uc2, test_res) ==  [(1, [1,2,2,2,3,3,4,4]), (2, [1,1,2,3,3,3,4,4]),
                                            (3, [1,1,2,2,3,4,4,4]), (4, [2,2,2,2,3,3,4,4]),
                                            (5, [1,2,2,3,3,3,4,4]), (6, [1,2,2,2,3,4,4,4]), 
                                            (7, [1,1,3,3,3,3,4,4]), (8, [1,1,2,3,3,4,4,4]), 
                                            (9, [1,1,2,2,4,4,4,4])]
    # Shouldn't change because of function call
    assert test_res == [1,1,2,2,3,3,4,4]

def test_check_pcs():
    def mpc(x):
        return PointCard(0, x)

    # Can only buy if resources are enough for one
    assert check_pcs([mpc([])],[])
    assert check_pcs([mpc([])],[1,2,2])
    assert check_pcs([mpc([2,2])],[]) == False
    assert check_pcs([mpc([1,2,3])],[2,3]) == False
    assert check_pcs([mpc([1,2,3])],[1,2,3])
    assert check_pcs([mpc([1,1,3])],[1,3]) == False
    # True if can pay for at least one
    assert check_pcs([mpc([1,1,3]), mpc([1,2,3])],[1,1,3])
    assert check_pcs([mpc([1,1,2]), mpc([2,2,3])],[1,2,2,3])
    assert check_pcs([mpc([1,1,2]), mpc([2,2,3])],[1,1,2,2,3])
    assert check_pcs([mpc([1,1,2]), mpc([2,2,3])],[2]) == False

def test_pay_pcs():
    def mpc(x):
        return PointCard(0, x)
    card0 = mpc([])
    card1 = mpc([1,2,3])
    card2 = mpc([1,1,3])
    assert pay_pcs([card0],[]) == [card0]
    assert pay_pcs([mpc([2,2])],[]) == []
    assert pay_pcs([card1],[1,2,3]) == [card1]
    assert pay_pcs([mpc([1,1,3])],[1,3]) == []
    assert pay_pcs([card2, card1],[1,1,3]) == [card2]
    # Considers paying for both at the same time:
    assert pay_pcs([card1, card2],[1,1,2,2,3]) == [card1] 
    assert pay_pcs([card1, card2],[1,1,1,2,3,3]) == [card1, card2] 
    assert pay_pcs([mpc([1,1,2]), mpc([2,2,3])],[2]) == []
#@pytest.mark.skip()
def test_forw_astar():
    def follow_path(path, resources = None):
        if resources == None:
            resources = []
        for action in path:
            if action.type == ActionType.PLAY:
                action.card.playable = True
                multi_plays = play_card(action.card, resources)
                resources = multi_plays[action.times - 1][1]
        return resources
    
    ## Test 1
    card1 = MerchantCard([],[1])
    card2 = MerchantCard([],[2,3])
    path = forward_astar( [PointCard(0, [1,1]), PointCard(0, [1,2,3])], 
        [card1,MerchantCard([1],[]),card2], [2] )
    follow = follow_path(path, [2])
    assert check_pcs([PointCard(0, [1,1]), PointCard(0, [1,2,3])], follow)
    assert check_pcs([PointCard(0, [1,2,3])], follow)
    assert check_pcs([PointCard(0, [1,1])], follow) == False

    ## Test 2
    HAND2 = [
        MerchantCard([],reward=[1,1,1]),
        MerchantCard([],reward=[1,1]),
        MerchantCard([3,3],[4,4]),
        MerchantCard([2,2,2],[3,3,3]),
        MerchantCard([1,1],[2,2]),
        MerchantCard([4],[1,2,3])
    ]
    PCs2 = [PointCard(14,[1, 2, 3, 4])]
    RES2 = [2]

    path = forward_astar( PCs2, HAND2, RES2 )
    follow = follow_path(path, RES2)
    assert check_pcs(PCs2, follow)

    ## Test 3
    HAND3 = [
        MerchantCard([],[5,5]), 
        MerchantCard([4],[1,1]),
        MerchantCard([3],[2,1])
    ]
    PCs3 = [PointCard(14,[1,1,1])]
    RES3 = [1]

    path = forward_astar( PCs3, HAND3, RES3)
    follow = follow_path(path, RES3)
    assert check_pcs(PCs3, follow)

    ## Test 4
    HAND = [
        MerchantCard([],[1,1,1,1,1,1]), 
        MerchantCard([],[1,1,1,1,1])
    ]
    PCs = [PointCard(14,[1,1,1,1,1,1,1,1,1,1])]
    RES = []

    path = forward_astar( PCs, HAND, RES)
    follow = follow_path(path, RES)
    assert check_pcs(PCs, follow)
    assert len(path) == 3

    ## Test 5
    HAND = [
        MerchantCard([],[1]), 
        MerchantCard([],[2])
    ]
    PCs = [PointCard(14,[3])]
    RES = []

    path = forward_astar( PCs, HAND, RES)
    follow = follow_path(path, RES)
    assert follow == []
    assert len(path) == 0

    ## Test 6
    HAND = [
        MerchantCard([],reward=[1,1]),
        MerchantCard([],reward=[3]),
        MerchantCard([],[5,5])
    ]
    PCs = [PointCard(14,[2, 2, 2, 2, 3, 3])]
    RES = []

    path = forward_astar( PCs, HAND, RES, max_depth=8)
    follow = follow_path(path, RES)
    assert check_pcs(PCs, follow)
    assert len(path) == 8

    ## Test 7
    HAND = [
        MerchantCard([],[1,1])
    ]
    PCs = [PointCard(4, [1,1,1,1])]
    RES = [1,1]

    HAND[0]['playable'] = False
    path = forward_astar( PCs, HAND, RES, max_depth=4)
    assert len(path) == 3
    follow = follow_path(path, RES)
    assert check_pcs(PCs, follow)

def test_dfs():
    #TODO Write actual tests for dfs. What should they be? 
    HAND2 = [
        MerchantCard([],reward=[1,1]),
        MerchantCard([],reward=[3]),
        MerchantCard([],[5,5])
    ]
    PCs2 = [PointCard(14,[2, 2, 2, 2, 3, 3])]
    RES2 = []
    
    val = DFS( PCs2, HAND2, RES2, max_depth=8 )


def check_pcs(pcs, caravan):
    """
    Can resources pay for at least one of PointCards?
    """
    spices = Counter(caravan)
    return any(
        0 == sum( (Counter(pc['cost']) - spices) )
        for pc in pcs)
