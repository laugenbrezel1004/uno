import os
from Card import Card
from Computer import test
from Game import Game
from Human import Human

# Constants for game configuration
INITIAL_CARD_AMOUNT = 7  # Number of cards each player starts with


def clear_screen():
    """Clear the terminal screen based on operating system."""
    os.system('cls' if os.name == 'nt' else 'clear')


def is_playable(card: Card, game: Game) -> bool:
    """
    Determine if a card can be legally played on current stack top.

    Args:
        card (Card): Card to check
        game (Game): Current game state

    Returns:
        bool: True if card is playable
    """
    last_card = game.get_last_card()
    if not last_card:
        return True

    # Penalty rules override normal matching
    if game.penalty > 0:
        if card.symbol == '+2':
            return card.color == last_card.color or last_card.symbol == '+2'
        if card.symbol == '+4':
            return True
        return False

    # Normal UNO matching rules
    return (card.points >= 50 or  # Wild cards always playable
            last_card.color == 'RESET' or  # After wild card, anything goes
            card.color == last_card.color or
            card.symbol == last_card.symbol)


def main():
    """Entry point: Setup and start single-player UNO game."""
    name = input('Please enter your name: ')
    game = Game([Human(name), test()])
    game.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
