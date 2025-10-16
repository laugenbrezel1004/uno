import random
from typing import Optional, List
from Card import Card
from Player import Player
from collections import Counter
from Game import Game
from main import is_playable


class test(Player):
    """
    AI-controlled computer player with strategic card selection logic.
    Prioritizes action cards, color matching, and hand optimization.
    """

    def __init__(self):
        """Initialize computer player with default name 'Computer'."""
        super().__init__('Computer')

    def choose_color(self) -> str:
        """
        AI color selection: Choose most common color in hand for future plays.
        Falls back to random if no colored cards.
        """
        if not self.cards:
            return random.choice(['RED', 'GREEN', 'BLUE', 'YELLOW'])
        color_counts = Counter(card.color for card in self.cards if card.color != 'RESET')
        return max(color_counts, key=color_counts.get, default=random.choice(['RED', 'GREEN', 'BLUE', 'YELLOW']))

    def select_card(self, game: 'Game') -> Optional[List[Card]]:
        """
        AI decision making for card selection with strategic priorities:
        1. Call UNO when down to 2 cards (80% chance)
        2. Play +4 during penalties if possible
        3. Prefer action cards matching current color
        4. Play multiple identical cards when available
        5. Wild cards as last resort

        Args:
            game (Game): Current game instance

        Returns:
            Optional[List[Card]]: Cards to play or None to draw
        """
        # Strategic UNO calling
        if len(self.cards) == 2 and not self.called_uno and random.random() < 0.8:
            self.call_uno()

        playable_cards = [card for card in self.cards if is_playable(card, game)]
        if not playable_cards:
            return None

        # Group identical playable cards for stacking
        groups = {}
        for card in playable_cards:
            key = (card.color, card.symbol)
            if key not in groups:
                groups[key] = []
            groups[key].append(card)

        # Play largest group of identical cards
        max_group = max(groups.values(), key=len, default=[])
        if len(max_group) > 1:
            return max_group

        # Color frequency analysis for strategy
        color_counts = Counter(card.color for card in self.cards if card.color != 'RESET')

        def select_from_priority_group(cards: List[Card]) -> List[Card]:
            """Select preferred card from group based on color strategy."""
            if not cards:
                return None
            if len(cards) > 1:
                most_common_color = max(color_counts, key=color_counts.get, default=None)
                if most_common_color:
                    preferred_cards = [card for card in cards if card.color == most_common_color]
                    if preferred_cards:
                        return [random.choice(preferred_cards)]
            return [random.choice(cards)]

        last_card = game.get_last_card()

        # Priority 1: Handle penalties with +4
        if game.penalty > 0:
            plus4_cards = [card for card in playable_cards if card.symbol == '+4']
            if plus4_cards:
                return [random.choice(plus4_cards)]
            return select_from_priority_group(playable_cards)

        # Priority 2: Action cards matching color
        action_cards_color_match = [card for card in playable_cards if
                                    card.symbol in ('R', 'S', '+2') and card.color == last_card.color]
        if action_cards_color_match:
            return select_from_priority_group(action_cards_color_match)

        # Priority 3: Number cards matching color
        number_cards_color_match = [card for card in playable_cards
                                    if isinstance(card.symbol, str) and card.symbol.isdigit() and
                                    card.color == last_card.color]
        if number_cards_color_match:
            return select_from_priority_group(number_cards_color_match)

        # Priority 4: Symbol matching (non-wild)
        symbol_match_cards = [card for card in playable_cards if
                              card.symbol == last_card.symbol and card.symbol not in ('C', '+4')]
        if symbol_match_cards:
            return select_from_priority_group(symbol_match_cards)

        # Priority 5: Action cards matching symbol
        action_cards_symbol_match = [card for card in playable_cards
                                     if card.symbol in ('R', 'S', '+2') and card.symbol == last_card.symbol]
        if action_cards_symbol_match:
            return select_from_priority_group(action_cards_symbol_match)

        # Priority 6: Wild cards (prefer +4 when low on cards)
        wild_cards = [card for card in playable_cards if card.symbol in ('C', '+4')]
        if wild_cards:
            if len(self.cards) <= 3:
                plus4_cards = [card for card in wild_cards if card.symbol == '+4']
                if plus4_cards:
                    return [random.choice(plus4_cards)]
            return [random.choice(wild_cards)]

        return select_from_priority_group(playable_cards)
