
from century.source.SpiceAI import double_astar, DFS, forward_astar, game_search, goodness, play_upgrade, run_game, run_gamestate
import random
import os
from century.source.structures import Player, PointCard, GameState, MCs_from_file, MerchantCard, PCs_from_file
from century.source.helpers import random_game

def playground():
    curr_dir = os.path.dirname(__file__)
    with open(os.path.join(curr_dir, 'century/resources/MerchantCards.txt')) as f:
        mcs = MCs_from_file(f)
    with open(os.path.join(curr_dir, 'century/resources/PointCards.txt')) as f:
        pcs = PCs_from_file(f)
    
    for i in range(15):
        random.seed(18)
        gs, p = random_game(mcs[3:], pcs, hand_size= 5)
        # print(p.hand[3])
        path = run_gamestate(gs, p)
        # path = game_search(gs, p)
        print(i)
    print(path)
    
def tokenize_game(gs:GameState, p:Player):
    # Use pickle for general serializing. .compress for NN input layers
    # import pickle
    path = forward_astar(gs.point_list, p.hand, p.caravan, MCs = gs.merchant_list)
    return gs.compress() + p.compress() + str(len(path))    

def simple_game():
    # Simple Game to PLay
    HAND3 = [
        MerchantCard([],[5,5]), 
        MerchantCard([4],[1,1]),
        MerchantCard([3],[2,1])
    ]
    PCs3 = [PointCard(14,[1,1,1])]
    RES3 = [1,1]

    print(DFS(PCs3, HAND3, RES3, max_depth=4))

def drop_10_game():
    # Game that requires a lot of drop_10
    pcl = [PointCard(15, [3,3,3,3,3]), PointCard(10, [1,1,4,4])]
    hand = [
        MerchantCard([],[1,3]),
        MerchantCard([3],[1,1,1,1,2]),
        MerchantCard([1,1,1],[2,2,2]),
        MerchantCard([2,2,2],[4,4]),
        MerchantCard([4],[3,3]),
        MerchantCard([],[1,1]),
        MerchantCard([],[5,5])
    ]
    caravan = [1,1,1]

    print(forward_astar(pcl, hand, caravan, max_depth=7))
    print(DFS(pcl, hand, caravan, max_depth=7))

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

def prof():
    import cProfile
    import pstats
    profile = cProfile.Profile()
    profile.enable()
    
    playground()

    #
    # End Doc Profiling code
    #
    profile.disable()
    p = pstats.Stats(profile)
    p.strip_dirs().sort_stats('time').print_stats(10)
    p.sort_stats('time').print_callers(3)
    
if __name__ == '__main__':
    try:
        prof()
    except (EOFError,KeyboardInterrupt) as e:
        print("\nGoodbye! Play again soon")
        exit(e)
