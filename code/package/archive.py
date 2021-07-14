"""
Never include this. Purely a place to store old functions until deletion
"""


### DEEP BFS; ITERATIVE; w/ COPY July 12th
def deep_search(pc_list, hand, caravan, MCs = None, max_depth = 8):
    """
    Extended version of forward_astar that looks through all options in max_depth
    (avoiding some Nodes with dynamic programming). Because it comes from a
    BFS A* algorithm there's a lot of slow copying that can be avoided with the
    new DFS.
    """
    frontier = Queue()
    frontier.put(Node(caravan, Path(), hand, pc_list) )
    found = {}
    while not frontier.empty():
        currentNode: Node = frontier.get()

        if len(currentNode.path) == max_depth:
            frontier.put(currentNode)
            break
        
        # try_score(Node) -> list[Nodes to explore]
        children = try_score(currentNode)
        # try_play(Node) -> list[Nodes to explore]
        children.extend(try_play(currentNode))
        # try_reclaim(Node) -> list[Nodes to explore]
        children.extend(try_reclaim(currentNode))
        # try_buy(Node, list[MerchantCards]) -> list[Nodes to explore]
        if MCs: children.extend(try_buy(currentNode, MCs))
        for child in children:
            pursue_if_better(child, found, frontier)

    final = []
    while not frontier.empty():
        i: Node = frontier.get()
        if i.path.score() > 0:
            final.append(i)
    
    # Default for if nothing can be found
    if len(final) == 0:
        if MCs:
            return Path(Action(ActionType.BUY, MCs[0]))
        else:
            return Path()

    scores = []
    for i, option in enumerate(final):
        scores.append( (goodness(option), i))
    return final[ sorted(scores, reverse=True)[0][1] ].path


# OLD RUN GAME USING FORWARD A* FOR EACH CARD
# def run_game(...):
    # path = forward_astar(PCs, hand, resources)
    # def find_better_trades(path: Path, PCs, hand, resources, MCs):
    #     for i in range(min(resources.count(1),len(MCs))):
    #         hand.append(MCs[i])
    #         for _ in range(i): resources.remove(1)     
    #         temp = forward_astar(PCs, hand, resources)          
    #         if len(temp) > 0:
    #             # I don't like this. Should Path handle its own inserting?
    #             temp.set_front(Action(ActionType.BUY, MCs[i]))
    #         resources = [1]*i + resources
    #         for card in hand:
    #             card.playable = True
    #         hand.pop()
    #         if len(temp) > 0 and (len(temp) < len(path) or len(path) == 0):
    #             path = temp
    #     return path
    # path = find_better_trades(path, PCs, hand, resources, MCs)
    

def backwards_goal(card, curr_goal):
    """Based on the given Merchant Card, remove the rewards from curr_goal 
    then add in the cost to the goal. 

    Returns the new goal (maybe modifies the original) and boolean if "helped"."""
    progress = False
    for resource in card.get('reward'):
        try:
            curr_goal.remove(resource)
            progress = True
        finally:
            continue
    for resource in card.get('cost'):
        curr_goal.append(resource)
    return curr_goal, progress


def play_forward(pc_list, hand, resources, max_depth = 8, pc_dict = None, path = None):
    """
    See how many point cards you can get to from current hand in
    max_depth plays. Can include starting resources later.
    """
    if pc_dict == None:
        pc_dict = {}
    if path == None:
        path = []
    if max_depth <= 0:
        return False, pc_dict # reached end without finding
    max_depth -= 1
    #print(f"IN {str_hand(hand)} {resources} {max_depth}")
    for card in hand:
        played, resources = play_card(card, resources)
        if not played:
            continue
        card['playable'] = False
        path.append(card)
        matched_pcs = check_pcs(pc_list, resources)
        if matched_pcs:
            lst = pay_pcs(pc_list, resources)
            for pc in lst:
                str_pc = str(pc)
                if str_pc not in pc_dict or max_depth < pc_dict[str_pc]:
                    pc_dict[str_pc] = max_depth
            print_forward_path(path)
            return True, pc_dict
        downstream, down_dict = play_forward(pc_list, hand, resources, max_depth, pc_dict, path)
        path.pop()
        card['playable'] = True
        if downstream:
            return True, pc_dict
        resources, worked = backwards_goal(card, resources)
        if not worked:
            raise ValueError("Bad backing up")

    max_depth -= 1
    for card in hand:
        card['playable'] = True
    path.append("PICK UP")
    downstream, _ = play_forward(pc_list, hand, resources, max_depth, pc_dict, path)
    if downstream:
        return True, pc_dict
    
    return False, pc_dict

# June 2, replaced by Path()
def play_forward_astar(pc_list, hand, resources, max_depth = 8):
    frontier = PriorityQueue()
    frontier.put(Node(0, resources, [], hand) )
    found = {}
    while not frontier.empty():
        currentNode : Node = frontier.get()
        if len(currentNode.path) > max_depth:
            break
        if check_pcs(pc_list, currentNode.goal): # make more complicated with multiple cards found
            return currentNode.path
        # Generate child nodes
        for i, card in enumerate(currentNode.hand):
            # If child shouldn't be pursued, skip
            played, new_resources = play_card(card, currentNode.goal)
            if not played:
                continue
                     
            def copy_to_child(parent : Node, index, new_resources) -> Node:
                '''Make a child Node from parent with copy of card at index with 'playable' set to False.'''
                copy_hand = [x.copy() for x in parent.hand]
                new_card = copy_hand[index]
                new_card['playable'] = False
                new_path = list(parent.path)
                new_path.append(new_card)
                priority = len(new_path) #- heuristic(new_resources)
                return Node( priority, new_resources, new_path, copy_hand)

            # Copy everything into a new Node
            child = copy_to_child(currentNode, i, new_resources)
            
            # Only pursue if child is better than found, 
            key = repr(child.goal)
            if key not in found or child.priority < found[key]:
                found[key] = child.priority
                frontier.put(child)
            
        # Pick up cards
        for card in currentNode.hand:
            card['playable'] = True
        new_path = list(currentNode.path)
        new_path.append("PICK UP")
        priority = len(new_path) + max_depth #+ heuristic(currentNode.goal)
        frontier.put(Node(priority, currentNode.goal, new_path, currentNode.hand))
    
    return f"A connecting path less than {max_depth} doesn't exist :("

# June 2, back a_star removed because front is more intuitive
def a_star(point_card, hand, max_depth = 8):
    '''A* search starting with a goal set by point_card and working
    back max_depth card plays till the goal is empty.'''

    if not point_card['cost']: return "That was easy! Free!"  
    frontier = PriorityQueue()
    frontier.put( Node(0,point_card['cost'],[],hand) )
    found = {}
    counter =0 
    while not frontier.empty():
        node = frontier.get()
        curr_hand = node.hand
        if len(node.path) >= max_depth:
            break
        for card in curr_hand:
            if not card['playable']: # abstract this?
                continue
            new_goal, useful = backwards_goal(card, node.goal.copy())
            if not useful or len(new_goal) > 10: # abstract this constraint
                continue
            new_path = list(node.path)
            copy_hand = [x.copy() for x in curr_hand]
            new_card = copy_hand[curr_hand.index(card)]
            new_card['playable'] = False
            new_path.append(new_card)
            priority = len(new_path) + heuristic(new_goal)
            if not new_goal:
                print(counter)
                return new_path
            key = repr(new_goal)
            if key not in found or priority < found.get(key):
                found[key] = priority
                frontier.put( Node(priority, new_goal, new_path, copy_hand) )  
                counter+=1
        # Pick up cards
        for card in curr_hand:
            card['playable'] = True
        new_path = list(node.path)
        new_path.append("PICK UP")
        priority = len(new_path) + heuristic(node.goal)
        frontier.put(Node(priority,node.goal,new_path,curr_hand.copy()))
        counter+=1
        

    return f"A connecting path less than {max_depth} doesn't exist :("

def test_back_astar():
    """Asserts to make sure backward A* matching is working"""
    hand = [
        MerchantCard([],[1,1]),
        MerchantCard([],[1,2])
    ]
    assert a_star(PointCard(20,[]), hand) == 'That was easy! Free!'
    assert a_star(PointCard(20,[1]), hand)[0]['reward'] == [1,1]
    assert a_star(PointCard(20,[1,2]), hand)[0]['reward'] == [1,2]
    assert a_star(PointCard(20,[1,1]), hand)[0]['reward'] == [1,1]

    hand2 = [
        MerchantCard([1,1,1],[4]),
        MerchantCard([],[1,1,1])
    ]   
    assert len(a_star(PointCard(14,[1,1,4,4]), hand2)) == 7 # with PICK UP
