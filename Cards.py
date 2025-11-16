from enum import Enum
from typing import List

# ANSI color codes for terminal card display
COLORS = {
    'WHITE': '\033[47m',
    'BLACK': '\033[1;30m',
    'RED': '\033[1;31m',
    'GREEN': '\033[1;32m',
    'YELLOW': '\033[1;33m',
    'BLUE': '\033[1;34m',
    'RESET': '\033[0m'
}


class CardType(Enum):
    NUMBER = 1
    SKIP = 2
    REVERSE = 3
    DRAW_TWO = 4
    WILD = 5
    WILD_DRAW_FOUR = 6

class CardSuits(Enum):
    RED = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4



class Card:

    def __init__(self, card_type: CardType, suit: CardSuits = None, card_number = None):
        self.suit: CardSuits = suit
        self.type_of_card: CardType = card_type
        self.card_number = card_number