"""
Two strategy
"""
import random
import math
from game import Game


def interactive_strategy(game: Game) -> str:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def random_strategy(game: Game) -> str:
    """
    randomly return a possible move from the current state
    """
    poss = game.current_state.get_possible_moves()
    rand = math.floor(random.random() * len(poss))
    return poss[rand]


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config="a1_pyta.txt")
