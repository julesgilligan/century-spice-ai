"""
Class structures for the GameState and Player
"""
from century.classes.cards import MerchantCard, PointCard, COMPLENG_P, COMPLENG_M
from century.helpers.switch import Caravan
from dataclasses import dataclass

@dataclass
class GameState():
    merchant_list: list[MerchantCard]
    point_list: list[PointCard]
    silver: int = 8
    gold: int = 8

    def compress(self):
        """Length 79:\n
        6 Merchant Cards, 9 length each (0-53)\n
        5 Point Cards, 5 length each (54-78)"""
        string = ''.join(mc.compress() for mc in self.merchant_list)
        if len(self.merchant_list) < 6:
            string += (6 - len(self.merchant_list))*COMPLENG_M*'0'
        string += ''.join(pc.compress() for pc in self.point_list)
        if len(self.point_list) < 5:
            string += (5 - len(self.point_list))*COMPLENG_P*'0'
        if len(string) != (COMPLENG_M*6 + COMPLENG_P*5):
            raise ValueError(f"GameState compression is {len(string)} not expected {(COMPLENG_M*6 + COMPLENG_P*5)}")
        return string

@dataclass
class Player():
    caravan: Caravan
    hand: list[MerchantCard]
    score: int = 0
    point_count: int = 0

    def compress(self, hand_size = 4):
        """Length default 40: 4 caravan + 9*hand_size (0-39)"""
        string = str(hex(self.caravan.count(1)).split('x')[-1])
        string+= str(hex(self.caravan.count(2)).split('x')[-1])
        string+= str(hex(self.caravan.count(3)).split('x')[-1])
        string+= str(hex(self.caravan.count(4)).split('x')[-1])
        string+= ''.join(mc.compress() for mc in self.hand[:hand_size])
        if len(self.hand) < hand_size:
            string+= (hand_size - len(self.hand))*COMPLENG_M*'0'
        return string
    
    @staticmethod
    def starting_hand():
        return [MerchantCard([],[5,5]), MerchantCard([],[1,1])]

def str_hand(hand):
    return "| " + " | ".join(map(str, hand)) + " |"
