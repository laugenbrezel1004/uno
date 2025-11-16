import sys

from Game import Game
from Player import Player

if __name__ == '__main__':

    try:
        running_game = Game()
        running_game.run()

    except KeyboardInterrupt:
       print("\nBye!")
       sys.exit()
    except Exception as e:
        print(f"some weird error {e}")




