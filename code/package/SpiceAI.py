'''
Century Spice Road AI

Century Spice Road is a straightforward game of getting Point Cards by spending
certain combinations of resources. Resources come in odd combinations from Merchant
Cards.
'''
from collections import Counter
from itertools import combinations_with_replacement
from queue import PriorityQueue

from .structures import Action, ActionType, GameState, MerchantCard, Node, NodeMutable, Path, Player, PointCard

def double_astar(pc_list, hand, caravan, MCs = None, max_depth = 8):
    good, result = forward_astar(pc_list, hand, caravan, MCs = MCs, max_depth = max_depth)
    if len(result) < max_depth:
        good, result = forward_astar(pc_list, hand, caravan, MCs = MCs, max_depth = (max_depth - len(result)), start_path = result)
    return good, result

def forward_astar(pc_list, hand, caravan, **kwargs):
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
    frontier.put(Node(caravan, start_path, hand, pc_list) )
    found = {}
    while not frontier.empty():
        currentNode: Node = frontier.get()
        if len(currentNode.path) == max_depth:
            break

        # Action: Score
        ts = try_score(currentNode)
        if ts != []:
            return goodness(ts[0]), ts[0].path # try_score sorts highest value first

        # Action: Play
        # Generate child nodes from valid card plays
        children = try_play(currentNode)
        # Action: Reclaim
        # One child from picking up all cards
        children.extend(try_reclaim(currentNode))
        if MCs:
            children.extend(try_buy(currentNode, MCs))
        for child in children:
            pursue_if_better(child, found, frontier)
    return goodness(Node(caravan, start_path, hand, pc_list)), start_path

### DFS, RECURSIVE, w/o COPY

def game_search(gs: GameState, p: Player, max_depth = 8):
    return DFS(gs.point_list, p.hand, p.caravan, gs.merchant_list, max_depth)

def DFS(pc_list, hand, caravan, MCs = None, max_depth = 8) -> Path:
    """
    API entrance for running one player search by DFS. Returns the best Path
    (by the goodness function) and should be faster than previous A* attempts
    """
    found = {}
    node_count = [0]
    global tree
    tree = [0]*(max_depth + 1)
    result = dfs_recursive(NodeMutable(caravan, Path(), hand, pc_list), MCs, found, max_depth, node_count)
    # print("DFS count (all nodes):", node_count[0])
    # print("tree (explored nodes)",tree[::-1], sum(tree))
    # print("Goodness: ", goodness(result))
    return goodness(result), result.path

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
            new_goal = child.goal
            for x in pc['cost']:
                new_goal.remove(x)
            yield child
            for x in pc['cost']:
                new_goal.append(x)
            new_goal.sort()
            curr.drop_last()
        return True
    
    def yield_play(currentNode):
        for i, card in enumerate(currentNode.hand):
            multi_plays = play_card(card, currentNode.goal)
            # If card can't be played, skip
            if not multi_plays:
                continue
            old_cl = currentNode.goal
            for num_play, cubes in multi_plays:
                if len(cubes) <= 10:
                    lst_of_lsts = [cubes]
                else:
                    lst_of_lsts = drop_to_10(cubes)    
                
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
        for i in range(min(currentNode.goal.count(1),len(MCs))):
            mc = MCs[i]
            if mc in currentNode.hand:
                continue
            if 0 == sum( Counter(mc['cost']) - Counter(currentNode.goal) ):
                child = currentNode.new_with(
                    path = currentNode.path.add(Action(ActionType.BUY, card = mc)),
                    hand = currentNode.hand + [MCs[i]]
                )

                caravan = child.goal
                for _ in range(i): caravan.remove(1)
                yield child
                for _ in range(i): caravan.append(1)
                caravan.sort()
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
                    best_node =  Node(result.goal, result.path, result.hand, result.pcs)

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
        new_goal = child.goal
        for x in pc['cost']:
            new_goal.remove(x)
        child_list.append(child)
    return child_list

def pay_pcs(pcs: list[PointCard], resources) -> list[PointCard]:
    """
    Which PointCards can resources pay for? Pays for in given order, caller sort by cost
    """
    running_list = []
    res = Counter(resources)
    for pc in pcs:
        pcc = Counter(pc['cost'])
        if 0 == sum((pcc - res).values()):
            running_list.append(pc)
            res -= pcc # remove already paid resources
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
            if len(cubes) <= 10:
                lst_of_lsts = [cubes]
            else:
                lst_of_lsts = drop_to_10(cubes)    
            
            for cl in lst_of_lsts:
                child = copy_to_child(currentNode, i, cl, num_play)
                child_list.append(child)
    return child_list

def play_card(card: MerchantCard, resources):
    """Forward play a card. Returns a list[ (plays, resources) ] or False if impossible"""
    if not card['playable']: 
        return False
    if card.is_upgrade():
        return play_upgrade(card, resources)
   
    caravan = Counter(resources)
    cost = Counter(card['cost'])
    reward = Counter(card['reward'])
    if len(card['cost']) > 0:
        # Trades can be done multiple times
        multiples = min(
            caravan[key] // cost[key]
            for key in cost.keys()
        )
        if multiples == 0:
            return False
    else:
        # Free receives only go once
        multiples = 1

    pursue = [None]*multiples
    for i in range(multiples):
        caravan -= cost
        caravan += reward
        pursue[i] = (i+1, sorted(caravan.elements())) 

    return pursue

def play_upgrade(upgrade, resources):
    cnt = upgrade['reward'].count(5)
    effective_cards = [MerchantCard([1],[2]), MerchantCard([2],[3]), MerchantCard([3],[4])]

    def play_once(c):
        # 'caravan' comes from play_upgrade scope
        if caravan.count( c['cost'][0]) > 0:
            caravan.remove(c['cost'][0])
            caravan.append(c['reward'][0])
            caravan.sort()
            return True
        return False

    pursue = []
    index = 1
    for num in range(cnt):
        for comb in combinations_with_replacement(effective_cards, num + 1):
            caravan = resources.copy()
            # If this combination of upgrades can all be played, save it
            if all( map(play_once, comb) ):
                pursue.append( (index, caravan) )
                index += 1

    if pursue == []:
        return False
    return pursue

def copy_to_child(parent : Node, index, new_resources, num_plays) -> Node:
    '''Make a child Node from parent with copy of card at index with 'playable' set to False.'''
    child = parent.new_with(
        path = parent.path.add(Action(ActionType.PLAY, parent.hand[index], plays=num_plays)),
        caravan = new_resources
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
    for i in range(min(currentNode.goal.count(1),len(MCs))):
        mc = MCs[i]
        if mc in currentNode.hand:
            continue
        if 0 == sum( Counter(mc['cost']) - Counter(currentNode.goal) ):
            child = currentNode.new_with(
                path = currentNode.path.add(Action(ActionType.BUY, card = mc)),
                hand = currentNode.hand + [MCs[i]]
            )
            caravan = child.goal
            for _ in range(i): caravan.remove(1)
            children.append(child)
    return children

##
## Small functions to help clean things up
##

def found_key(state: Node):
    string = ''.join(map(str,state.goal)).ljust(10,'0')
    string += 'S:' + str(state.path.score())
    # string += 'L:' + str(len(state.path)) # makes sure to not over skip, but adds checks
    string += ''.join('1' if c['playable'] else '0' for c in state.hand) 
    return string

def pursue_if_better(child, found, frontier):
    key = found_key(child)
    if key not in found or child.priority < found[key]:
        found[key] = child.priority
        frontier.put(child)
   
def drop_to_10(cubes):
    ret = []
    for choice in combinations_with_replacement([1,2,3,4], len(cubes) - 10):
        try:
            new_cubes = cubes.copy()
            for cube in choice:
                new_cubes.remove(cube)
            ret.append(new_cubes)
        except ValueError:
            continue
    return ret

def goodness(node: Node):
    score = node.path.score()
    score_turns = node.path.score_turn()
    buy = len(node.hand)
    spices = sum(node.goal)
    # 1 turn < buy one card < 2 turns
    # 1 turn < +2 pt < 3 turn
    # 2 spice < buy < 6 spice
    return 4*score + sum( -4*x for x in score_turns ) + 5*buy + spices
