import os
import time
from typing import List

from Card import Card, COLORS
from Computer import test
from Player import Player
from Deck import Deck
from Human import Human
from main import is_playable, clear_screen


def _clear_screen() -> None:
    """Clear terminal screen."""
    clear_screen()


class Game:
    """
    Main game controller managing turn order, stack, penalties, and game flow.
    Handles single-player mode (human vs computer) with full UNO rules.
    """
    INITIAL_CARD_AMOUNT = 7

    def __init__(self, players: List[Player]):
        """
        Initialize game with players, deck, and starting conditions.

        Args:
            players (List[Player]): List of players (must be exactly 2 for single-player)

        Raises:
            ValueError: Invalid number of players or insufficient cards
        """
        if not players:
            raise ValueError("At least one player is required.")
        if len(players) != 2:
            raise ValueError("Single-player mode requires exactly two players (human and computer).")

        self.deck = Deck()
        if len(self.deck.cards) < len(players) * self.INITIAL_CARD_AMOUNT + 1:
            raise ValueError("Deck does not have enough cards for all players and stack.")

        # Player management
        self.players = {player.player_id: player for player in players}
        self.player_ids = list(self.players.keys())
        self.current_player_index = 0
        self.current_player_id = self.player_ids[self.current_player_index]
        self.turn_direction = 1  # 1=forward, -1=reverse
        self.human_player_id = next(pid for pid, p in self.players.items() if isinstance(p, Human))

        # Game state
        self.stack = []  # Played cards (top card at index 0)
        self.penalty = 0  # Draw penalty from +2/+4 cards
        self.opponent_skip = 0  # Skip turns from Skip/Reverse
        self.pending_uno_penalty = None  # Player ID for UNO penalty
        self.uno_penalty_warning = ""
        self.uno_penalty_applied = ""
        self.game_message = ""

        # Setup initial game state
        self._initialize_stack()
        self._deal_initial_cards()

    def _initialize_stack(self) -> None:
        """
        Draw initial stack card, ensuring it's a regular number card (0-9).
        Special cards are returned to deck until valid card found.
        """
        while True:
            if not self.deck.cards:
                raise ValueError("Deck is empty, cannot initialize stack.")
            card = self.deck.draw()
            if card.get_points() <= 9:  # Number card only
                self.stack.insert(0, card)
                break
            self.deck.cards.append(card)
            self.deck.shuffle()

    def _deal_initial_cards(self) -> None:
        """Deal initial hand to all players."""
        for player in self.players.values():
            cards = [self.deck.draw() for _ in range(self.INITIAL_CARD_AMOUNT)]
            player.add_cards(cards)

    def reverse_turn_order(self) -> None:
        """Reverse turn direction (for >2 players) and adjust current player."""
        self.turn_direction *= -1
        self.current_player_index = (self.current_player_index - self.turn_direction) % len(self.player_ids)

    def set_uno_penalty_warning(self, message: str) -> None:
        """Set warning message for potential UNO penalty."""
        self.uno_penalty_warning = message

    def set_uno_penalty_applied(self, message: str) -> None:
        """Set message when UNO penalty is applied."""
        self.uno_penalty_applied = message

    def set_game_message(self, message: str) -> None:
        """Set temporary game message (skip, penalty, etc.)."""
        self.game_message = message

    def set_opponent_skip(self, amount: int):
        """Set number of opponent turns to skip."""
        self.opponent_skip = amount

    def run(self):
        """Main game loop handling turns until a winner is found."""
        while True:
            player = self.players[self.current_player_id]
            self.game_message = ""  # Clear messages each turn

            # Handle pending UNO penalties
            if self.pending_uno_penalty and self.pending_uno_penalty != self.current_player_id:
                penalized_player = self.players[self.pending_uno_penalty]
                self.set_uno_penalty_applied(f"{penalized_player.name} forgot to call UNO! Drawing 2 cards as penalty.")
                penalized_player.add_cards([self.deck.draw() for _ in range(2)])
                self.pending_uno_penalty = None
                self.print_game_screen(self.human_player_id)
                time.sleep(1.5)
                self.set_uno_penalty_applied("")

            # Handle skip effects
            if self.opponent_skip > 0:
                self.opponent_skip -= 1
                self.set_game_message(f"{player.name} has been skipped!")
                self.print_game_screen(self.human_player_id)
                time.sleep(1.5)
            else:
                self.print_game_screen(self.human_player_id)
                if self.play_turn(player):
                    print(f'{player.name} won!')
                    break

            time.sleep(2)
            # Advance to next player
            self.current_player_index = (self.current_player_index + self.turn_direction) % len(self.player_ids)
            self.current_player_id = self.player_ids[self.current_player_index]
            self.uno_penalty_warning = ""

    def play_turn(self, player: Player) -> bool:
        """
        Execute a single player's turn including penalty handling and drawing.

        Args:
            player (Player): Current player

        Returns:
            bool: True if player won, False otherwise
        """
        print(f"{player.name}'s turn")
        try:
            if self.penalty > 0:
                # Handle penalty: try to play +2/+4 or draw cards
                cards = player.select_card(self)
                if cards and is_playable(cards[0], self):
                    player.play_cards(cards, self)
                    self.print_game_screen(self.human_player_id)
                else:
                    self.set_game_message(f"{player.name} must draw {self.penalty} cards as penalty!")
                    penalty_cards = [self.deck.draw() for _ in range(self.penalty)]
                    player.add_cards(penalty_cards)
                    self.penalty = 0
                    self.print_game_screen(self.human_player_id)
                    print(f'{player.name} drew {len(penalty_cards)} cards.')
                    # Check if can play after drawing
                    if isinstance(player, Human):
                        cards = player.prompt_play_after_draw(self)
                    else:
                        cards = player.select_card(self)
                    if cards and is_playable(cards[0], self):
                        player.play_cards(cards, self, end_turn=True)
                        self.print_game_screen(self.human_player_id)
            else:
                # Normal turn: play card or draw one
                cards = player.select_card(self)
                if cards and is_playable(cards[0], self):
                    player.play_cards(cards, self)
                    self.print_game_screen(self.human_player_id)
                else:
                    drawn_card = self.deck.draw()
                    player.add_cards([drawn_card])
                    self.print_game_screen(self.human_player_id)
                    if is_playable(drawn_card, self):
                        if isinstance(player, Human):
                            cards = player.prompt_play_after_draw(self, drawn_card)
                        else:
                            cards = player.select_card(self)
                        if cards and is_playable(cards[0], self):
                            player.play_cards(cards, self, end_turn=True)
                            self.print_game_screen(self.human_player_id)
                        else:
                            self.set_game_message(f"{player.name} kept the drawn card...")
                    else:
                        self.set_game_message(f"{player.name} drew a card that is not playable...")
            return player.has_won()
        except ValueError as e:
            print(f"Error in turn: {str(e)}")
            time.sleep(1)
            return False

    def get_last_card(self):
        """Get the top card from the stack."""
        return self.stack[0] if self.stack else None

    def get_player_cards(self) -> List[Card]:
        """Get human player's cards for display."""
        return self.players[self.human_player_id].cards

    def get_computer_cards(self) -> List[Card]:
        """Get computer player's cards."""
        computer_id = next(pid for pid, p in self.players.items() if isinstance(p, test))
        return self.players[computer_id].cards

    def print_game_screen(self, player_id: str) -> None:
        """
        Render complete game UI from human player's perspective.

        Args:
            player_id (str): Human player ID

        Raises:
            ValueError: Invalid player or non-human player
        """
        if player_id not in self.players:
            raise ValueError(f"Player {player_id} not found.")
        if not isinstance(self.players[player_id], Human):
            raise ValueError("Game screen can only be displayed for human player in single-player mode.")

        _clear_screen()
        terminal_width = self._get_terminal_width()
        cards_per_row = max(1, terminal_width // 10)

        # Display opponent hand (hidden)
        self._display_opponent_hands(player_id, cards_per_row)

        # Display game stack
        self._display_stack(cards_per_row)

        # Display player hand with numbers
        self._display_player_hand(player_id, cards_per_row)

        # Show warnings and status
        if self.penalty > 0 and self.current_player_id == player_id:
            print(f"Warning: Penalty active! You must draw {self.penalty} cards or play a +2/+4.")

        # UNO status
        for pid, player in self.players.items():
            if player.called_uno:
                print(f"{player.name} has called UNO!")

        # Game messages
        if self.game_message:
            print(self.game_message)
        if self.uno_penalty_warning:
            print(self.uno_penalty_warning)
        if self.uno_penalty_applied:
            print(self.uno_penalty_applied)

    def _get_terminal_width(self) -> int:
        """Get current terminal width for responsive layout."""
        return os.get_terminal_size().columns

    def _display_opponent_hands(self, player_id: str, cards_per_row: int) -> None:
        """Show opponent card counts and hidden card backs."""
        for pid, player in self.players.items():
            if pid != player_id:
                print(f"Player {player.name}'s hand: {len(player.cards)} cards")
                self._display_hidden_cards(player.cards, cards_per_row)

    def _display_hidden_cards(self, cards: List[Card], cards_per_row: int) -> None:
        """
        Display hidden card backs for opponents using generic hidden card template.

        Args:
            cards (List[Card]): Opponent's cards (not actually used, just count)
            cards_per_row (int): Cards to display per row
        """
        for i in range(0, len(cards), cards_per_row):
            row_cards = cards[i:i + cards_per_row]
            full_lines = [''] * 7
            for _ in row_cards:
                lines = Card('?', 'RESET', 0).generate(hidden=True)
                for j in range(7):
                    full_lines[j] += lines[j] + ' ' + COLORS['RESET']
            print('\n'.join(full_lines) + '\n\n')

    def _display_stack(self, cards_per_row: int) -> None:
        """Display the game stack (recently played cards)."""
        print("Board:")
        game_stack = self.stack[:8]  # Show last 8 cards max
        board_rows = []
        for i in range(0, len(game_stack), cards_per_row):
            row_cards = game_stack[i:i + cards_per_row]
            full_lines = [''] * 7
            for index, card in enumerate(row_cards):
                lines = card.generate() if index == 0 else card.generate_short()
                for j in range(7):
                    full_lines[j] += lines[j] + ' ' + COLORS['RESET']
            board_rows.append('\n'.join(full_lines))
        print('\n\n'.join(board_rows) + '\n')

    def _display_player_hand(self, player_id: str, cards_per_row: int) -> None:
        """
        Display human player's hand with card numbers for selection.

        Args:
            player_id (str): Human player ID
            cards_per_row (int): Cards per display row
        """
        print("Hand:")
        player = self.players[player_id]
        player_rows = []
        number_lines = []
        for i in range(0, len(player.cards), cards_per_row):
            row_cards = player.cards[i:i + cards_per_row]
            full_lines = [''] * 7
            for card in row_cards:
                lines = card.generate()
                for j in range(7):
                    full_lines[j] += lines[j] + ' ' + COLORS['RESET']
            player_rows.append('\n'.join(full_lines))

            # Add card numbers
            number_line = ''
            for j in range(len(row_cards)):
                card_number = j + 1 + i
                number_str = f"{card_number}."
                padding = (10 - len(number_str)) // 2
                number_line += ' ' * padding + number_str + ' ' * (10 - padding - len(number_str)) + COLORS['RESET']
            number_lines.append(number_line)

        for row, num_line in zip(player_rows, number_lines):
            print(row)
            print(num_line)
        print()
