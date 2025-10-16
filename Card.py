from typing import List, Optional, Dict

# ANSI color codes for terminal card display
COLORS = {
    'WHITE': '\033[47m',
    'BLACK': '\033[1;30m',
    'RED': '\033[1;31m',
    'GREEN': '\033[1;32m',
    'YELLOW': '\033[1;33m',
    'BLUE': '\033[1;34m',
    'RESET': '\033[0m'
}
class Card:
    """
    Represents a single UNO card with symbol, color, and point value.
    Handles visual representation and generation of ASCII art for display.
    """

    def __init__(self, symbol: str, color: str, points: int):
        """
        Initialize a card with its symbol, color, and point value.

        Args:
            symbol (str): Card symbol (e.g., '5', 'R', '+2', 'C')
            color (str): Card color ('RED', 'GREEN', 'BLUE', 'YELLOW', 'RESET')
            points (int): Point value for scoring
        """
        self.symbol = symbol
        self.color = color
        self.points = points

    def get_points(self) -> int:
        """Return the point value of the card."""
        return self.points

    def __repr__(self) -> str:
        """Simple colored string representation for debugging."""
        return f'{COLORS["WHITE"] if self.color == "BLACK" else ""}{COLORS[self.color]}{self.symbol}{COLORS["RESET"]}'

    def generate(self, hidden=False) -> List[str]:
        """
        Generate ASCII art representation of the card as a list of 7 lines.

        Args:
            hidden (bool): If True, show '?' instead of actual symbol

        Returns:
            List[str]: 7 lines representing the card visually
        """
        value = str(self.symbol) if not hidden else '?'
        color = COLORS[self.color] if not hidden else COLORS['RESET']
        border_t = color + '┌' + '─' * 7 + '┐'
        border_b = color + '└' + '─' * 7 + '┘'
        empty = color + '│' + ' ' * 7 + '│'
        if len(value) == 2:
            rank = color + '│' + ' ' + value + ' ' * 4 + '│'
            r_rank = color + '│' + ' ' * 4 + value + ' ' + '│'
        else:
            rank = color + '│' + ' ' + value + ' ' * 5 + '│'
            r_rank = color + '│' + ' ' * 5 + value + ' ' + '│'
        return [border_t, rank, empty, empty, empty, r_rank, border_b]

    def generate_short(self):
        """Generate a compact version of the card for board display."""
        return [COLORS[self.color] + "───┐",
                COLORS[self.color] + "   │",
                COLORS[self.color] + "   │",
                COLORS[self.color] + "   │",
                COLORS[self.color] + "   │",
                COLORS[self.color] + (self.symbol if len(self.symbol) == 2 else ' ' + self.symbol) + " │",
                COLORS[self.color] + "───┘"]
