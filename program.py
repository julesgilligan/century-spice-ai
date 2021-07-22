
from code.package.SpiceAI import double_astar
import random
import os
from code.package import (DFS, GameState, MCs_from_file, MerchantCard,
                     PCs_from_file, forward_astar)
from code.package.structures import Player, PointCard
from code import random_game

def prof():
    import cProfile
    import pstats
    profile = cProfile.Profile()
    profile.enable()
    #
    # End Doc Profiling code
    #
    playground()

    profile.disable()
    p = pstats.Stats(profile)
    p.strip_dirs().sort_stats('time').print_stats(10)
    p.sort_stats('time').print_callers(3)
    
def tokenize_game(gs:GameState, p:Player):
    # Use pickle for general serializing. .compress for NN input layers
    # import pickle

    path = forward_astar(gs.point_list, p.hand, p.caravan, MCs = gs.merchant_list)
    return gs.compress() + p.compress() + str(len(path))

def playground():
    curr_dir = os.path.dirname(__file__)
    with open(os.path.join(curr_dir, 'code/package/MerchantCards.txt')) as f:
        mcs = MCs_from_file(f)
    with open(os.path.join(curr_dir, 'code/package/PointCards.txt')) as f:
        pcs = PCs_from_file(f)
    
    gs, p = random_game(mcs[3:], pcs, hand_size= 5)
    print(len(tokenize_game(gs, p)) -1)
    # for pc in gs.point_list:
    #     print(pc)
    # print(p.caravan)
    # for c in p.hand:
    #     print(c)
    # print(DFS(gs.point_list, p.hand, p.caravan, gs.merchant_list))

    ## Game that requires a lot of drop_10
    ##
    # pcl = [PointCard(15, [3,3,3,3,3]), PointCard(10, [1,1,4,4])]
    # hand = [
    #     MerchantCard([],[1,3]),
    #     MerchantCard([3],[1,1,1,1,2]),
    #     MerchantCard([1,1,1],[2,2,2]),
    #     MerchantCard([2,2,2],[4,4]),
    #     MerchantCard([4],[3,3]),
    #     MerchantCard([],[1,1]),
    #     MerchantCard([],[5,5])
    # ]
    # caravan = [1,1,1]

    # print(deep_search(pcl, hand, caravan, max_depth=7))
    # print(DFS(pcl, hand, caravan, max_depth=7))


    # # Simple Game to PLay
    # HAND3 = [
    #     MerchantCard([],[5,5]), 
    #     MerchantCard([4],[1,1]),
    #     MerchantCard([3],[2,1])
    # ]
    # PCs3 = [PointCard(14,[1,1,1])]
    # RES3 = [1,1]

    # print(DFS(PCs3, HAND3, RES3, max_depth=4))

def compare_three():
    with open('package/MerchantCards.txt') as f:
        mcs = MCs_from_file(f)
    with open('package/PointCards.txt') as f:
        pcs = PCs_from_file(f)

    import time

    print("Index, Hand, Depth, G A*, G DFS, S A*, S DFS, T A*, T DFS")
    for i in range(11,31):
        hand_size = random.randint(4,7)
        gs, p = random_game(mcs[3:], pcs, hand_size)
        depth = random.randint(6,9)
        
        # A*
        start = time.process_time()
        good_a, path_a = double_astar(gs.point_list, p.hand, p.caravan, MCs=gs.merchant_list, max_depth=depth)
        score_a = path_a.score()
        time_a = time.process_time() - start

        # Depth search
        start = time.process_time()
        good_d, path_d = DFS(gs.point_list, p.hand, p.caravan, MCs=gs.merchant_list, max_depth=depth)
        score_d = path_d.score()
        time_d = time.process_time() - start

        print(f"{i}, {hand_size}, {depth}, {good_a}, {good_d}, {score_a}, {score_d}, {time_a}, {time_d}")


def run_game(PCs, hand, resources, MCs):
    PCs = [x for x in PCs if isinstance(x, PointCard)]
    hand = [x for x in hand if isinstance(x, MerchantCard)]
    resources = [x for x in resources if x in [1,2,3,4]]
    MCs = [x for x in MCs if isinstance(x, MerchantCard)]

    path = DFS(PCs, hand, resources, MCs)

    return path


if __name__ == '__main__':
    try:
        # prof()
        playground()
        # compare_three()
        #main()
    except (EOFError,KeyboardInterrupt) as e:
        print("\nGoodbye! Play again soon")
        exit(e)
