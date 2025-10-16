import time
from typing import Optional, List

from Game import Game
from Player import Player
from Card import COLORS, Card
from main import is_playable


class Human(Player):
    """
    Human player implementation with interactive input handling.
    Provides console interface for card selection and color choice.
    """

    def choose_color(self) -> str:
        """Prompt user to select a color for wild cards."""
        while True:
            action = input(
                f'Which color do you choose? {COLORS["RED"]}(R)ed{COLORS["RESET"]}, '
                f'{COLORS["GREEN"]}(G)reen{COLORS["RESET"]}, '
                f'{COLORS["BLUE"]}(B)lue, {COLORS["YELLOW"]}(Y)ellow{COLORS["RESET"]}: '
            ).upper()
            color = {'R': 'RED', 'G': 'GREEN', 'B': 'BLUE', 'Y': 'YELLOW'}.get(action)
            if color:
                return color
            print("Invalid color. Please enter R, G, B, or Y.")
            time.sleep(1)

    def select_card(self, game: 'Game') -> Optional[List[Card]]:
        """
        Handle human player's card selection through interactive prompts.

        Args:
            game (Game): Current game instance

        Returns:
            Optional[List[Card]]: Selected cards or None to draw
        """
        while True:
            self._print_game_state(game)
            action = self._get_valid_action()
            if action == 'U':
                self.call_uno()
                cards = self._handle_play_action(game)
                if cards:
                    return cards
                continue
            elif action == 'P':
                cards = self._handle_play_action(game)
                if cards:
                    return cards
                continue
            else:  # 'D'
                return None

    def _print_game_state(self, game: 'Game') -> None:
        """Display current game state for human player."""
        game.print_game_screen(self.player_id)

    def _get_valid_action(self) -> str:
        """Get valid action from human input: Play, Draw, or UNO."""
        while True:
            action = input('(P)lay or (D)raw a card or call (U)no: ').upper()
            if action in ('P', 'D', 'U'):
                return action
            print("Invalid input. Please enter 'P', 'D' or 'U'.")
            time.sleep(1)

    def _handle_play_action(self, game: 'Game') -> Optional[List[Card]]:
        """
        Handle the actual card selection process for playing.

        Args:
            game (Game): Current game instance

        Returns:
            Optional[List[Card]]: Selected playable cards or None
        """
        if not self.cards:
            print("No cards to play!")
            time.sleep(1)
            return None

        # Check playable cards
        playable_cards = [card for card in self.cards if is_playable(card, game)]
        if not playable_cards:
            print("You have no playable cards!")
            time.sleep(1)
            return None

        while True:
            input_str = input('Card? (e.g., 1, 1+2, "u" for UNO, "r" to return): ')
            if input_str.lower() == 'u':
                self.call_uno()
                continue
            if input_str.lower() == 'r':
                return None
            try:
                indices = [int(idx) - 1 for idx in input_str.split('+')]
                selected_cards = [self.cards[idx] for idx in indices if 0 <= idx < len(self.cards)]
                if len(selected_cards) != len(indices):
                    print("Invalid card number.")
                    time.sleep(1)
                    continue
                if len(selected_cards) > 1:
                    # Multiple cards must be identical
                    first_card = selected_cards[0]
                    if not all(card.color == first_card.color and card.symbol == first_card.symbol for card in
                               selected_cards):
                        print("Selected cards are not identical.")
                        time.sleep(1)
                        continue
                card = selected_cards[0]
                if not is_playable(card, game):
                    print("Card isn't playable.")
                    time.sleep(1)
                    continue
                return selected_cards
            except ValueError:
                print("Invalid input. Enter a number or numbers separated by '+'. ")
                time.sleep(1)

    def prompt_play_after_draw(self, game: 'Game', drawn_card: Optional[Card] = None) -> Optional[List[Card]]:
        """
        After drawing a card, prompt human to play it if possible or check other cards.

        Args:
            game (Game): Current game instance
            drawn_card (Optional[Card]): Card just drawn

        Returns:
            Optional[List[Card]]: Cards to play or None
        """
        if drawn_card and is_playable(drawn_card, game):
            while True:
                self._print_game_state(game)
                choice = input(f"You drew {drawn_card}. Call UNO or play? (U)no, (Y)es, (N)o: ").upper()
                if choice == 'U':
                    self.call_uno()
                    continue
                if choice in ('Y', 'N'):
                    return [drawn_card] if choice == 'Y' else None
                print("Invalid input. Please enter 'U', 'Y', or 'N'.")
                time.sleep(1)
        elif any(is_playable(card, game) for card in self.cards):
            while True:
                self._print_game_state(game)
                play = input("You have playable cards. Call UNO or play? (U)no, (Y)es, (N)o: ").upper()
                if play == 'U':
                    self.call_uno()
                    continue
                if play == 'N':
                    return None
                if play != 'Y':
                    print("Invalid input. Please enter 'U', 'Y', or 'N'.")
                    time.sleep(1)
                    continue
                return self._handle_play_action(game)
        else:
            print('No playable cards...')
            time.sleep(1)
            return None
