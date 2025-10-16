from Cards import Card, CardSuits, CardType
import random


class Deck:

    def __init__(self):

        # cards that have been thrown and are ready to be shuffled back in
        self.storage_pile: list[Card] = []

        # cards that can be pulled from
        self.holding_deck: list[Card] = []
        #iterate through the different types of suits

        # e.g. red, blue, green, yellow
        for suit in CardSuits:
            # get the colored numbers
            for i in range(0, 10):
                self.holding_deck.append(Card(CardType.NUMBER,suit, i))
            for i in range(1, 10):
                self.holding_deck.append(Card(CardType.NUMBER,suit, i))

            #color wildcards
            for i in range(0,2):
                self.holding_deck.append(Card(CardType.SKIP, suit))

            for i in range(0,2):
                self.holding_deck.append(Card(CardType.REVERSE, suit))
            for i in range(0,2):
                self.holding_deck.append(Card(CardType.DRAW_TWO, suit))

        # black wildcards
        for i in range(0,4):
            self.holding_deck.append(Card(CardType.WILD))
        for i in range(0,4):
            self.holding_deck.append(Card(CardType.WILD_DRAW_FOUR))

        for card in self.holding_deck:
            print(f"card suit: {card.suit} | card type: {card.type_of_card} | value of number: {card.card_number}")

        self.shuffle()




    def shuffle(self):
        random.shuffle(self.holding_deck)
        for card in self.holding_deck:
            print(f"card suit: {card.suit} | card type: {card.type_of_card} | value of number: {card.card_number}")
