import random
from Card import COLORS
from typing import List
from Card import Card

class Deck:
    """
    Manages the UNO card deck, including initialization, shuffling, and drawing.
    Creates standard UNO deck with duplicates and special cards.
    """

    def __init__(self):
        """Initialize and populate the deck with standard UNO cards."""
        self.cards: List[Card] = []
        self.init_cards()

    def init_cards(self):
        """Create a standard UNO deck with number cards, action cards, and wild cards."""
        self.cards = []
        # Number cards 0-9 (two of each per color)
        for i in range(10):
            for color in ['RED', 'GREEN', 'BLUE', 'YELLOW']:
                self.cards.extend([Card(str(i), color, i)] * 2)

        # Action cards (Reverse, Skip, +2 - two of each per color)
        for color in ['RED', 'GREEN', 'BLUE', 'YELLOW']:
            self.cards.extend([Card('R', color, 25) for _ in range(2)])
            self.cards.extend([Card('S', color, 35) for _ in range(2)])
            self.cards.extend([Card('+2', color, 45) for _ in range(2)])

        # Wild cards (Color Change and +4 - four of each, no color)
        self.cards.extend([Card('C', 'RESET', 50) for _ in range(4)])
        self.cards.extend([Card('+4', 'RESET', 70) for _ in range(4)])
        self.shuffle()

    def shuffle(self):
        """Randomly shuffle the deck."""
        random.shuffle(self.cards)

    def draw(self) -> Card:
        """
        Draw and return the top card from the deck.

        Raises:
            ValueError: If deck is empty
        """
        if not self.cards:
            raise ValueError("Deck is empty!")
        return self.cards.pop()

    def __repr__(self) -> str:
        """String representation of all cards in deck (for debugging)."""
        return ''.join(card.__repr__() + COLORS['RESET'] for card in self.cards)
