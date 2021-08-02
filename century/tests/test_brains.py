"""
tests for the various functions. Run 'pytest' in shell from the project directory
"""
from century.classes import ActionType, MerchantCard, PointCard
from century.core.SpiceAI import DFS, forward_astar, play_card

from .test_smalls import check_pcs, play_card

def test_forw_astar():
    ## Test 1
    # Play card 1,3 before 1,R,1
    HAND = [
        MerchantCard([],[1]),
        MerchantCard([1],[]),
        MerchantCard([],[2,3])
    ]
    PCs =[ 
        PointCard(0, [1,1]), PointCard(0, [1,2,3])
    ]
    RES = [2]
    path = forward_astar( PCs, HAND, RES )
    follow = follow_path(path, RES)
    assert check_pcs(PCs, follow)
    assert check_pcs([PCs[0]], follow) == False
    assert check_pcs([PCs[1]], follow)
    assert len(path) == 3

    ## Test 2
    # Use a lot of cards out of order
    # (1|2),5,4,3,6
    HAND = [
        MerchantCard([],reward=[1,1,1]),
        MerchantCard([],reward=[1,1]),
        MerchantCard([3,3],[4,4]),
        MerchantCard([2,2,2],[3,3,3]),
        MerchantCard([1,1],[2,2]),
        MerchantCard([4],[1,2,3])
    ]
    PCs = [PointCard(14,[1, 2, 3, 4])]
    RES = [2]

    # path, follow = run_test( 
    #         hand = ["->111", {,11}, {33,44}, {222,333}, {11,22}, {4,123}],
    #         point_cards = ["14 1234"],
    #         caravan = [2],
    #         expected_len = 6
    # )

    path = forward_astar( PCs, HAND, RES )
    follow = follow_path(path, RES)
    assert check_pcs(PCs, follow)
    assert len(path) == 6

    ## Test 3
    # still considers if over 10, and drops to exactly 10
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
    # TODO: This assert fails. Find out why.
    # assert len(follow) == 10

    ## Test 4
    # Can't find this PointCard
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

def test_forw_reclaiming():
    ## Test 1
    # A little reclaiming
    # 1,3,R,1,2
    HAND = [
        MerchantCard([],[5,5]), 
        MerchantCard([4],[1,1]),
        MerchantCard([3],[2,1])
    ]
    PCs = [PointCard(14,[1,1,1])]
    RES = [1]

    path = forward_astar( PCs, HAND, RES)
    follow = follow_path(path, RES)
    assert check_pcs(PCs, follow)
    assert len(path) == 6

    ## Test 2
    # Get it in exactly the right amount
    # 1,2,3,R,1,2,3
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

    ## Test 3
    # Start with an unplayable card
    # R,1
    HAND = [
        MerchantCard([],[1,1])
    ]
    PCs = [PointCard(4, [1,1,1,1])]
    RES = [1,1]

    HAND[0]['playable'] = False
    path = forward_astar( PCs, HAND, RES, max_depth=4)
    follow = follow_path(path, RES)
    assert check_pcs(PCs, follow)
    assert len(path) == 3

def test_forw_buy():
    ## Test 1
    HAND = [
        MerchantCard([],reward=[1, 3])
    ]
    MCs = [
        MerchantCard([], [3]),
        MerchantCard([1], [1]),
        MerchantCard([], [2,2])
    ]
    PCs = [PointCard(14,[1, 2, 2])]
    RES = [1, 1]

    path = forward_astar( PCs, HAND, RES, MCs= MCs, max_depth=4)
    follow = follow_path(path, RES)
    assert check_pcs(PCs, follow)
    assert len(path) == 4
    assert path.score == 14

    ## Test 2
    # Needs to pick up both 1->3 and ->22. 
    # (BAD) Can score either in length but goes for 10 because it's first
    # (BAD) Could score with fewer cubes if it knows 1->3 makes ->22 cheaper
    HAND = [
    ]
    MCs = [
        MerchantCard([1], [3]),
        MerchantCard([1], [1]),
        MerchantCard([], [2,2])
    ]
    PCs = [PointCard(10,[2, 2, 3, 3]), PointCard(13,[2, 2, 2, 3])]
    RES = [1, 1, 1, 1]

    path = forward_astar( PCs, HAND, RES, MCs= MCs, max_depth=5)
    follow = follow_path(path, RES)
    assert path.score == 10
    assert check_pcs(PCs, follow)
    assert len(path) == 5

    ## Test 3
    # Needs to pick up both 1->3 and ->22
    HAND = [ ]
    MCs = [
        MerchantCard([1], [3]),
        MerchantCard([1], [1]),
        MerchantCard([], [2,2])
    ]
    PCs = [PointCard(10,[2, 2, 3, 3]), PointCard(13,[1, 2, 2, 3])]
    RES = [1, 1, 1, 1]

    path = forward_astar( PCs, HAND, RES, MCs= MCs, max_depth=5)
    follow = follow_path(path, RES)
    assert path.score == 13
    assert check_pcs(PCs, follow)
    assert len(path) == 5


def test_dfs():
    #TODO Write actual tests for dfs. What should they be?
    ## Test 1
    HAND = [
        MerchantCard([],reward=[1,1,1]),
        MerchantCard([],reward=[1,1]),
        MerchantCard([3,3],[4,4]),
        MerchantCard([2,2,2],[3,3,3]),
        MerchantCard([1,1],[2,2]),
        MerchantCard([4],[1,2,3])
    ]
    PCs = [PointCard(14,[1, 2, 3, 4])]
    RES = [2]

    path = DFS( PCs, HAND, RES )
    follow = follow_path(path, RES)
    assert path.score == 14
    assert check_pcs(PCs, follow)

    ## Test 2
    HAND = [
        MerchantCard([],reward=[1,1])
    ]
    MCs = [ 
        MerchantCard([], [3]),
        MerchantCard([],reward=[2,2]) 
    ]
    PCs = [ PointCard(10, [2,2,2]) ]
    RES = [2]
    path = DFS( PCs, HAND, RES, MCs= MCs, max_depth= 4)
    follow = follow_path(path, RES)
    assert follow == [1,1,2,2,2]
    assert check_pcs(PCs, follow)

    ## Important DFS thing to figure out later. Should get it in 8 (123R123S)
    # HAND = [
    #     MerchantCard([],reward=[1,1]),
    #     MerchantCard([],reward=[3]),
    #     MerchantCard([],[5,5])
    # ]
    # PCs = [PointCard(14,[2, 2, 2, 2, 3, 3])]
    # RES = []
    
    # val = DFS( PCs, HAND, RES, max_depth=8 )
    # follow = follow_path(val, RES)
    # assert check_pcs(PCs, follow)

def follow_path(path, resources = None):
    if resources == None:
        resources = []
    for action in path:
        if action.type == ActionType.PLAY:
            action.card.playable = True
            multi_plays = play_card(action.card, resources)
            resources = multi_plays[action.times - 1][1]
    return resources
