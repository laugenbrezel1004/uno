from Cards import Card, CardSuits, CardType
from typing import List


class Deck:
    #
    INITIAL_DECK_SIZE = 108

    # cards that have been thrown and are ready to be shuffled back in
    storage_pile: list[Card] = []

    # cards that can be pulled from
    holding_deck: list[Card] = []



    def __init__(self):

        #iterate through the different types of suits

        # e.g. red, blue, green, yellow
        for suit in CardSuits:
            # get the colored numbers
            for i in range(0, 10):
                self.holding_deck.append(Card(suit, CardType.NUMBER, i))
            for i in range(1, 10):
                self.holding_deck.append(Card(suit, CardType.NUMBER, i))

            #color wildcards
            for i in range(0,2):
                self.holding_deck.append(Card(suit, CardType.SKIP))

            for i in range(0,2):
                self.holding_deck.append(Card(suit, CardType.REVERSE))
            for i in range(0,2):
                self.holding_deck.append(Card(suit, CardType.DRAW_TWO))

        # black wildcards
        for i in range(0,4):
            self.holding_deck.append(Card(suit, CardType.WILD))
        for i in range(0,4):
            self.holding_deck.append(Card(suit, CardType.WILD_DRAW_FOUR))

        for card in self.holding_deck:
            print(f"card suit: {card.suit} | card type: {card.type_of_card} | value of number: {card.card_number}")




    def shuffle(self):
        pass