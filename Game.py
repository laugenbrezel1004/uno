from Player import Player
from Deck import Deck



class Game:
    def __init__(self):

        self.players = [Player(), Player()]
        self.draw_deck = []
        deck = Deck()


    def run(self):
        pass