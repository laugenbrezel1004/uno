import random
import uuid
from typing import List, Optional

from Card import Card
from Game import Game


class Player:
    """
    Base class for players (human or computer).
    Manages hand of cards, UNO calling status, and basic gameplay actions.
    """

    def __init__(self, name: str):
        """
        Initialize player with name and empty hand.

        Args:
            name (str): Player's name
        """
        self.name = name
        self.cards: List[Card] = []
        self.player_id = str(uuid.uuid4())  # Unique identifier
        self.called_uno = False  # Tracks if player has called UNO

    def add_cards(self, cards: List[Card]) -> None:
        """Add cards to player's hand and reset UNO status if hand >= 2 cards."""
        self.cards.extend(cards)
        if len(self.cards) >= 2:
            self.called_uno = False

    def get_cards(self) -> List[Card]:
        """Return the player's current hand."""
        return self.cards

    def play_card(self, card: Card, game: 'Game') -> None:
        """
        Play a single card onto the stack and handle special card effects.

        Args:
            card (Card): Card to play
            game (Game): Current game instance

        Raises:
            ValueError: If card not in player's hand
        """
        if card not in self.cards:
            raise ValueError(f"Card {card} not in player's hand.")
        self.cards.remove(card)
        game.stack.insert(0, card)  # Play to top of stack

        # Handle special card effects
        if card.symbol == 'R':
            if len(game.players) > 2:
                game.reverse_turn_order()
                game.set_game_message(f"{self.name} played Reverse! Turn order reversed!")
            else:
                game.set_opponent_skip(1)
                game.set_game_message(f"{self.name} played Reverse! Skipping...")
        elif card.symbol == 'S':
            game.set_opponent_skip(1)
            game.set_game_message(f"{self.name} played Skip!")
        elif card.symbol == '+2':
            game.penalty += 2
            game.set_game_message(f"{self.name} played +2! Next player must draw 2 cards or play a +2/+4.")
        elif card.symbol in ('C', '+4'):
            card.color = self.choose_color()
            game.set_game_message(f"{self.name} chose {card.color}!")
            if card.symbol == '+4':
                game.penalty += 4
                game.set_game_message(f"{self.name} played +4! Next player must draw 4 cards or play a +4.")

        # Reset UNO status after playing (unless down to 1 card)
        if len(self.cards) >= 2:
            self.called_uno = False

    def play_cards(self, cards: List[Card], game: 'Game', end_turn: bool = True) -> None:
        """
        Play multiple identical cards (for stacking penalties).

        Args:
            cards (List[Card]): Cards to play
            game (Game): Current game instance
            end_turn (bool): Whether this ends the turn
        """
        if len(cards) == 0:
            return
        if end_turn and len(self.cards) - len(cards) == 1 and not self.called_uno:
            game.set_uno_penalty_warning(f"{self.name} forgot to call UNO! Penalty may apply if the next player plays.")
            game.pending_uno_penalty = self.player_id
        for card in cards:
            self.play_card(card, game)

    def choose_color(self) -> str:
        """Choose a color for wild cards. Override in subclasses."""
        return random.choice(['RED', 'GREEN', 'BLUE', 'YELLOW'])

    def select_card(self, game: 'Game') -> Optional[List[Card]]:
        """
        AI logic to select which card(s) to play. Override in subclasses.

        Args:
            game (Game): Current game instance

        Returns:
            Optional[List[Card]]: Cards to play or None to draw
        """
        return None

    def call_uno(self):
        """Call UNO when down to one card."""
        self.called_uno = True
        print(f"{self.name} called UNO!")

    def has_won(self) -> bool:
        """Check if player has won (no cards left)."""
        return len(self.cards) == 0

    def __repr__(self) -> str:
        """String representation showing name and card count."""
        return f"{self.name} ({len(self.cards)} cards)"
