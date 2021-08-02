import functools

from century.classes import MerchantCard, PointCard
from century.core.SpiceAI import pay_pcs, play_card, play_upgrade
from century.helpers.switch import Caravan


def caravan_second_arg(func):
    functools.wraps(func)
    def wrapper(a, lst):
        if not isinstance(lst, Caravan):
            return func(a, Caravan(lst))
        return func(a, lst)
    return wrapper

play_card = caravan_second_arg(play_card)
play_upgrade = caravan_second_arg(play_upgrade)
pay_pcs = caravan_second_arg(pay_pcs)

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
    assert pay_pcs([card0],[]) == card0
    assert pay_pcs([mpc([2,2])],[]) == False
    assert pay_pcs([card1],[1,2,3]) == card1
    assert pay_pcs([mpc([1,1,3])],[1,3]) == False
    assert pay_pcs([card2, card1],[1,1,3]) == card2
    assert pay_pcs([card1, card2],[1,1,2,2,3]) == card1

@caravan_second_arg
def check_pcs(pcs, caravan: Caravan):
    """
    Can resources pay for at least one of PointCards?
    """
    return any(
        caravan.pays_for(pc['cost'])
        for pc in pcs)
