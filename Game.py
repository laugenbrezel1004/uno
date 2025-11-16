from Player import Player, Type_Of_Player
from Decks import Decks



class Game:
    def __init__(self):
        """
        Creates a new game instance.

        Includes a drawing deck with the 108 uno cards.
        Creates the players as well with a hand deck player type and a name if not pc.
        """


        # deck holding playcards
        self.decks: Decks = Decks()
        self.players = [Player(type_of_player=Type_Of_Player.HUMAN, name="laurenz", hand_deck=[self.decks.holding_deck.pop() for _ in range(7)]),
                        Player(type_of_player=Type_Of_Player.COMPUTER, hand_deck=[self.decks.holding_deck.pop() for _ in range(7)]),]

    def run(self):
        while True:
            pass
        """
        Starts the game
        """

