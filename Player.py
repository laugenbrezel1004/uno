from Cards import Card
from enum import Enum
from typing import List

class Type_Of_Player(Enum):
    HUMAN = 0
    COMPUTER = 1

class Player:

    def __init__(self, type_of_player:Type_Of_Player, name=None, hand_deck: List[Card] = None):
        if hand_deck is None:
            hand_deck = []
        self.type_of_player = type_of_player
        self.name = name
        self.hand_deck = []





