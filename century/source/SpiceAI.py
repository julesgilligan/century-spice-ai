'''
Century Spice Road AI

Century Spice Road is a straightforward game of getting Point Cards by spending
certain combinations of resources. Resources come in odd combinations from Merchant
Cards.
'''
from collections import Counter
from itertools import combinations_with_replacement
from os import remove
from queue import PriorityQueue

from .path import Action, ActionType, Node, NodeMutable, Path
from .structures import GameState, MerchantCard, Player, PointCard
from .switch import Caravan, append_each, remove_each


def run_game(PCs, hand, resources, MCs):
    PCs = [x for x in PCs if isinstance(x, PointCard)]
    hand = [x for x in hand if isinstance(x, MerchantCard)]
    resources = [x for x in resources if x in [1,2,3,4]]
    MCs = [x for x in MCs if isinstance(x, MerchantCard)]

    path = double_astar(PCs, hand, resources, MCs)
    path = DFS(PCs, hand, resources, MCs)
    return path
    
def run_gamestate(gs: GameState, p: Player, max_depth=8):
    double_astar(gs.point_list, p.hand, p.caravan, MCs= gs.merchant_list, max_depth= max_depth)

def double_astar(pc_list, hand, cube_list, MCs = None, max_depth = 8):
    result = forward_astar(pc_list, hand, cube_list, MCs = MCs, max_depth = max_depth)
    if len(result) < max_depth:
        result = forward_astar(pc_list, hand, cube_list, MCs = MCs, max_depth = (max_depth - len(result)), start_path = result)
    return result

def forward_astar(pc_list, hand, cube_list, **kwargs):
    """
    Additional keyword arguments include:\n 
    MCs: list[MerchantCard] = None \n 
    max_depth: int = 8 \n 
    start_path: Path = None
    """
    start_path = kwargs.get('start_path', Path())
    MCs = kwargs.get('MCs', None)
    max_depth = kwargs.get('max_depth', 8)

    frontier = PriorityQueue()
    frontier.put(Node(cube_list, start_path, hand, pc_list) )
    found = {}
    while not frontier.empty():
        currentNode: Node = frontier.get()
        if len(currentNode.path) == max_depth:
            break

        # Action: Score
        ts = try_score(currentNode)
        if ts != []: return ts[0].path

        children = try_play(currentNode)
        children.extend(try_reclaim(currentNode))
        if MCs: children.extend(try_buy(currentNode, MCs))
        
        for child in children:
            pursue_if_better(child, found, frontier)
    return start_path

### DFS, RECURSIVE, w/o COPY

def game_search(gs: GameState, p: Player, max_depth = 8):
    return DFS(gs.point_list, p.hand, p.caravan, gs.merchant_list, max_depth)

def DFS(pc_list, hand, cube_list, MCs = None, max_depth = 8) -> Path:
    """
    API entrance for running one player search by DFS. Returns the best Path
    (by the goodness function) and should be faster than previous A* attempts
    """
    found = {}
    node_count = [0]
    global tree
    tree = [0]*(max_depth + 1)
    result = dfs_recursive(NodeMutable(cube_list, Path(), hand, pc_list), MCs, found, max_depth, node_count)
    return result.path

def dfs_recursive(curr: Node, MCs, found, max_depth, counter) -> Node:
    """
    Called by DFS() to recursively find the best path from 'curr'. Stores
    progress in 'found' to avoid overvisting. 
    """
    found[found_key(curr)] = (len(curr.path), curr.priority)
    tree[max_depth] += 1
    # if sum(tree) % 10000 == 0:
    #     print(counter[0])

    if max_depth < 1:
        return curr

    # Generator version of previous try_*()
    # These avoid copying by backtracing between returning neighbors  

    def yield_score(curr:Node):
        for pc in pay_pcs( sorted(curr.pcs, reverse=True), curr.goal):
            if curr.path.already_scored(pc):
                continue
            child = curr.new_with(
                path = curr.path.add(Action(ActionType.SCORE, pc))
            )
            remove_each(child.goal, pc['cost'])
            yield child
            append_each(child.goal, pc['cost'])
            curr.drop_last()
        return True

    def yield_play(currentNode):
        for i, card in enumerate(currentNode.hand):
            multi_plays = play_card(card, currentNode.goal)
            # If card can't be played, skip
            if not multi_plays:
                continue
            old_cl = currentNode.goal.copy()
            for num_play, cubes in multi_plays:
                lst_of_lsts = gen_10_cubes(cubes)    
                
                for cl in lst_of_lsts:
                    child = currentNode.new_with(
                        path = currentNode.path.add(Action(ActionType.PLAY, currentNode.hand[i], plays=num_play)),
                        caravan = cl
                    )
            
                    old_play = child.hand[i]['playable']
                    child.hand[i]['playable'] = False
                    yield child
                    child.hand[i]['playable'] = old_play
                    
                    child.drop_last()
            object.__setattr__(currentNode, 'goal', old_cl)
        return True

    def yield_reclaim(currentNode:Node):
        if all( map(lambda card : card['playable'], currentNode.hand) ):
            return False
            
        child = currentNode.new_with(
            path = currentNode.path.add(Action(ActionType.RECLAIM))
        )
        old_playable = [card['playable'] for card in child.hand]
        for card in child.hand:
            card['playable'] = True
        yield child 
        for i, card in enumerate(child.hand):
            card['playable'] = old_playable[i]
        child.drop_last()
        return True

    def yield_buy(currentNode: Node, MCs):
        if MCs == None:
            return False
        for i in range(min( currentNode.goal.count(1),len(MCs))):
            mc = MCs[i]
            if mc in currentNode.hand:
                continue
            if currentNode.goal.pays_for(mc['cost']):
                child = currentNode.new_with(
                    path = currentNode.path.add(Action(ActionType.BUY, card = mc)),
                    hand = currentNode.hand + [MCs[i]]
                )

                remove_each(child.goal, [1]*i )
                yield child
                append_each(child.goal, [1]*i )
                currentNode.hand.pop()
                currentNode.drop_last()
        return True

    best_node = Node([], Path(), [], [])

    for gen in (yield_score, yield_play, yield_reclaim, lambda x: yield_buy(x, MCs)):
        for child in gen(curr):
            # print( (8-max_depth)*"    ", str(child.path).split('\n')[-2], child.goal)
            counter[0] += 1
            key = found_key(child)
            if key not in found or child.priority < found[key][1]:
                result = dfs_recursive(child, MCs, found, max_depth - 1, counter)
                if goodness(result) > goodness(best_node):
                    # not clear why result.new_with doesn't work here
                    best_node = Node(result.goal, result.path, result.hand, result.pcs)

    return best_node

##
## Get neighbors from trying to SCORE
##

def try_score(curr:Node):
    child_list = []
    for pc in pay_pcs( sorted(curr.pcs, reverse=True), curr.goal):
        if curr.path.already_scored(pc):
            continue
        child = curr.new_with(
            path = curr.path.add(Action(ActionType.SCORE, pc))
        )
        try:
            remove_each(child.goal, pc['cost'])
        except Exception as e:
            raise e
        child_list.append(child)
    return child_list

def pay_pcs(pcs: list[PointCard], caravan) -> list[PointCard]:
    """
    Which PointCards can resources pay for? Pays for in given order, caller sort by cost
    """
    running_list = []
    res = caravan.copy()
    for pc in pcs:
        if res.pays_for(pc['cost']):
            running_list.append(pc)
            remove_each(res, pc['cost']) # remove already paid resources
    return running_list

##
## Get neighbors from trying to PLAY
##

def try_play(currentNode):
    child_list = []
    for i, card in enumerate(currentNode.hand):
        multi_plays = play_card(card, currentNode.goal)
        # If card can't be played, skip
        if not multi_plays:
            continue
        for num_play, cubes in multi_plays:
            lst_of_lsts = gen_10_cubes(cubes)    
            
            for cara_opt in lst_of_lsts:
                child = copy_to_child(currentNode, i, cara_opt, num_play)
                child_list.append(child)
    return child_list

def play_card(card: MerchantCard, caravan: Caravan):
    """Forward play a card. Returns a list[ (plays, caravan) ] or False if impossible"""
    if not card['playable']: 
        return False
    if card.is_upgrade():
        return play_upgrade(card, caravan)
    
    cost = Counter(card['cost']) # TODO? literally the only use of Counter() in SpiceAI
    if len(card['cost']) > 0:
        # Trades can be done multiple times
        multiples = min(
            caravan.count(key) // cost[key]
            for key in cost.keys()
        )
        if multiples == 0:
            return False
    else:
        # Free receives only go once
        multiples = 1

    pursue = [None]*multiples
    for i in range(multiples):
        remove_each(caravan, card['cost'])
        append_each(caravan, card['reward'])
        pursue[i] = (i+1, caravan.copy())
    # this section avoids copying by returning parent caravan to original status
    for i in range(multiples):
        append_each(caravan, card['cost'])
        remove_each(caravan, card['reward'])
    return pursue

def play_upgrade(upgrade, caravan):
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

    pursue = []
    index = 1
    for num in range(cnt):
        for comb in combinations_with_replacement(effective_cards, num + 1):
            car_cpy = caravan.copy()
            # If this combination of upgrades can all be played, save it
            if all( map(play_once, comb) ):
                pursue.append( (index, car_cpy) )
                index += 1

    if pursue == []:
        return False
    return pursue

def copy_to_child(parent : Node, index, new_cara, num_plays) -> Node:
    '''Make a child Node from parent with copy of card at index with 'playable' set to False.'''
    child = parent.new_with(
        path = parent.path.add(Action(ActionType.PLAY, parent.hand[index], plays=num_plays)),
        caravan = new_cara
    )
    child.hand[index]['playable'] = False
    return child

##
## Get neighbors from trying to RECLAIM
##

def try_reclaim(currentNode:Node):
    if all( map(lambda card : card['playable'], currentNode.hand) ):
        return []
          
    child = currentNode.new_with(
        path = currentNode.path.add(Action(ActionType.RECLAIM))
    )
    for card in child.hand:
        card['playable'] = True
    return [child]

##
## Get neighbors from trying to BUY
##

def try_buy(currentNode: Node, MCs):
    children = []
    for i in range(min( currentNode.goal.count(1),len(MCs))):
        mc = MCs[i]
        if mc in currentNode.hand:
            continue
        if currentNode.goal.pays_for(mc['cost']):
            child = currentNode.new_with(
                path = currentNode.path.add(Action(ActionType.BUY, card = mc)),
                hand = currentNode.hand + [MCs[i]]
            )
            remove_each(child.goal, [1]*i)
            children.append(child)
    return children

##
## Small functions to help clean things up
##

def found_key(state: Node):
    string = ''.join(str(state.goal)).ljust(4,'0')
    string += 'S:' + str(state.path.score)
    # string += 'L:' + str(len(state.path)) # makes sure to not over skip, but adds checks
    string += ''.join('1' if c['playable'] else '0' for c in state.hand) 
    return string

def pursue_if_better(child, found, frontier):
    key = found_key(child)
    if key not in found or child.priority < found[key]:
        found[key] = child.priority
        frontier.put(child)

def gen_10_cubes(caravan: Caravan):
    # Occasionally, compare this to a version that copies. It can sometimes be faster
    if len(caravan) <= 10:
        yield caravan
        return True
        
    for choice in combinations(caravan._inv, len(caravan) - 10):
        remove_each( caravan, choice )
        yield caravan
        append_each( caravan, choice )
    return True

def goodness(node: Node):
    score = node.path.score
    score_turns = node.path.score_turn()
    buy = len(node.hand)
    spices = sum(node.goal.elements())
    # 1 turn < buy one card < 2 turns
    # 1 turn < +2 pt < 3 turn
    # 2 spice < buy < 6 spice
    return 4*score + sum( -4*x for x in score_turns ) + 5*buy + spices

def combinations(seq, length):
    a = max(min(seq[0], length), 0)
    for w in range(a, -1, -1):
        b = max(min(seq[1], length-w), 0)
        for x in range(b, -1, -1):
            c = max(min(seq[2], length-w-x), 0)
            for y in range(c, -1, -1):
                d = max(min(seq[3], length-w-x-y), 0)
                for z in range(d, -1, -1):
                    if w+x+y+z == length:
                        yield [1]*w+[2]*x+[3]*y+[4]*z
    return True
