from enum import Enum
class Player:
    def __init__(self, name=None, type=None):
        self.hand_deck = []
        self.type = Enum("human", "computer")
