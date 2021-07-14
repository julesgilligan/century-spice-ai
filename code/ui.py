import re

from termcolor import colored

from package import MerchantCard, PointCard, str_hand
from package.structures import stringify_cubes
from program import run_game


def command_line_ui():
    print(colored("Hello! Let's play Century Spice Road", "cyan", None, ["bold"]))
    txt = input("Are we starting fresh or already playing? ")
    while not check_start(txt):
        txt = input("I didn't understand that. Please try again. ")
    
    start_choice = check_start(txt)
    if start_choice in ['Start', 'Middle']:
         # Start path
        if start_choice == "Start":
            hand = [MerchantCard([],[5,5]),MerchantCard([],[1,1])]
            print("Okay, let's start.")
            print("\tI know your {}.\n\tI want to know your {}, available {}, and {}."
                .format(bold('hand'), bold('cubes'), bold('trades'), bold('point cards')))

        # Middle path
        elif start_choice == "Middle":
            print("Okay, please catch me up.")
            print("\tI want to know your {}, {}, available {}, and {}."
                .format( bold('hand'), bold('cubes'), bold('trades'), bold('point cards')))
            hand = get_hand()
   
        # get cubes, trades, and point cards
        resources = get_cubes()
        print("-"*80)
        print(f"\tYour hand is {str_hand(hand)}. \n\tYour cubes are {stringify_cubes(resources)}.")
        MCs = get_trades()
        print("-"*80)
        print(f"\tYour hand is {str_hand(hand)}. \n\tYour cubes are {stringify_cubes(resources)}. \n\tThe trades are {str_hand(MCs)}.")
        PCs = get_point_cards()
    
    elif start_choice == 'Debug':
        hand = [MerchantCard([],[5,5]),MerchantCard([],[1,1])]
        resources = [1,1,1]
        MCs = []
        PCs = [PointCard(17, [1,2,3,4])]

    while True:
        # Modifying prior input
        txt = ""
        while check_modify(txt) != 'Run':
            print("-"*80)
            print(f"\tYour hand is {str_hand(hand)}. \n\tYour cubes are {stringify_cubes(resources)}. \n\tThe trades are {str_hand(MCs)}.")
            print(f"\tThe point cards: {''.join((str(pc) for pc in PCs))}.")
            print("Type help for the list of commands")
            txt = input(">>")

            mod = check_modify(txt)
            if mod == None:
                print("Didn't catch that. Try again.")
                continue
            
            if mod == "Hand":
                hand = get_hand()
            elif mod == "Cube":
                resources = get_cubes()
            elif mod =="Trade":
                MCs = get_trades()
            elif mod =="Points":
                #PCs = get_point_cards()
                buy_pc_replace(PCs)
            elif mod == "Help":
                print("help, hand, cubes, trades, points, run")
            
        
        # Time to run it
        print("-"*80) 
        print("Okay. Let's run it. Looking out 8 turns.")
        path = run_game(PCs, hand, resources, MCs)

        if len(path) > 0:
            print("Try playing this path:")
            print(path)
        else:
            print("Didn't find anything. Change some things to try again.")


def check_start(txt):
    dic = {'Start' : '(fresh|new|start(?!e))',
        'Middle' : '(already|(ed)$|cont|(ing)$)',
        'Debug' : 'debug'
        }
    return re_search_with(dic, txt)

def check_modify(txt):
    dic = {'Hand' : '(hand|my cards)',
        'Cube' : '(cube|resource|spice)',
        'Trade' : '(trade|merchant|purple|bottom)',
        'Points' : '(point|orange|yellow|top)',
        'Run' : '(no|^n$|proceed|play|run)',
        'Help' : 'help'
        }
    return re_search_with(dic, txt)

def re_search_with(dic, txt):
    for key, value in dic.items():
        if re.search(value, txt, flags=re.IGNORECASE):
            return key
    return None

def get_cubes():
    confirm = 'N'
    while confirm.upper() != 'Y':
        txt = input(f"What are your cubes? (ex. {colored('1','yellow')} {colored('2', 'red')} {colored('3', 'green')} {colored('4', 'magenta')}) \t")
        cubes = [int(x) for x in re.findall('[1-4]{1}', txt)[:10]]
        confirm = input(f"Are these your cubes? (Y/N) {str(cubes)} \t")
    cubes.sort()
    return cubes

def get_trades():
    return get_cards(
        "Tell me the 6 available trades, cheapest first (ex. 123->33 \\n or 123,33)",
        6,
        read_merchant_card)

def get_point_cards():
    return get_cards(
        "Tell me the 5 point cards, furthest first (ex. 17 4 4 4 4 or 17, 4444)",
        5,
        read_point_card)

def get_cards(msg, count, func):
    confirm = 'N'
    confirm = 'N'
    while confirm.upper() != 'Y':
        print(msg)
        lst = []
        for i in range(count):
            card = func()
            if not card:
                break
            lst.append(card)
            print(lst[i])
        confirm = input("Are these the cards? (Y/N)\t")
    return lst

def get_hand():
    confirm = 'N'
    while confirm.upper() != 'Y':
        count = input("How many cards do you have? ")
        count = re.findall('(\d{1,2})', count)
        if count:
            count = int(count[0])
        else:
            continue
        print(f"What are your {count} cards? (ex. 123->33 \\n or 123,33)")
        lst = []
        for _ in range(count):
            card = read_merchant_card()
            if not card:
                break
            lst.append(card)
        confirm = input("Is this your hand? (Y/N)\t")
    return lst

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

def buy_pc_replace(lst):
    index = input("Which card has been removed (1-5)? ")
    index = int(re.match('[1-5]{1}', index)[0])
    if not index:
        print("That card number didn't make sense")
        return
    txt = input("What card replaced it?\n")
    card = read_point_card(txt)
    if card is None:
        print("Couldn't make that card")
        return
    lst.pop(index-1)
    lst.append(card)

def bold(string):
    return colored(string, None, None, ["bold"])
