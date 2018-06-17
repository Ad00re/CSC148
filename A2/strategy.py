"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
from typing import Any
import copy


def rough_outcome_strategy(game: Any) -> Any:
    """
    Return a move for game by picking a move which results in a state with
    the lowest rough_outcome() for the opponent.

    NOTE: game.rough_outcome() should do the following:
        - For a state that's over, it returns the score for the current
          player of that state.
        - For a state that's not over:
            - If there is a move that results in the current player winning,
              return 1.
            - If all moves result in states where the other player can
              immediately win, return -1.
            - Otherwise; return a number between -1 and 1 corresponding to how
              'likely' the current player will win from the current state.

        In essence: rough_outcome() will only look 1 or 2 states ahead to
        'guess' the outcome of the game, but no further. It's better than
        random, but worse than minimax.
    """
    current_state = game.current_state
    best_move = None
    best_outcome = -2  # Temporarily -- just so we can replace this easily later

    # Get the move that results in the lowest rough_outcome for the opponent
    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)

        # We multiply the below by -1 since a state that's bad for the opponent
        # is good for us.
        guessed_score = new_state.rough_outcome() * -1
        if guessed_score > best_outcome:
            best_outcome = guessed_score
            best_move = move

    # Return the move that resulted in the best rough_outcome
    return best_move

# TODO: Adjust the type annotation as needed.
def interactive_strategy(game: Any) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)

# TODO: Implement a recursive version of the minimax strategy.


def recursive_strategy(game: Any)->Any:
    """
    return a move that maximize the winning possible using recursion
    """
    curr = game.current_state
    dic = {}
    for item in curr.get_possible_moves():
        new_game = copy.deepcopy(game)
        new_game.current_state = new_game.current_state.make_move(item)
        dic[item] = -recur(new_game)
    max_chose = curr.get_possible_moves()[0]
    maxi = dic[max_chose]
    for item in curr.get_possible_moves():
        if dic[item] > maxi:
            max_chose = item
            maxi = dic[max_chose]
    return max_chose


def recur(game: Any)->Any:
    """
    The recursion part for the recursion strategy
    """
    if game.is_over(game.current_state):
        cur = game.current_state.get_current_player_name()
        if cur == 'p1':
            other = 'p2'
        else:
            other = 'p1'
        if game.is_winner(cur):
            return game.current_state.WIN
        elif game.is_winner(other):
            return game.current_state.LOSE
        return game.current_state.DRAW
    maxi = []
    for x in game.current_state.get_possible_moves():
        new_game = copy.deepcopy(game)
        new_game.current_state = game.current_state.make_move(x)
        maxi.append(-recur(new_game))
    return max(maxi)


class Tree:
    """
    a container that store a state and all possible next state
    """
    def __init__(self, game: Any)->None:
        """
        init a new tree
        """
        self.game = game
        self.score = None
        self.children = []

# TODO: Implement an iterative version of the minimax strategy.


def iterative_strategy(game: Any)->Any:
    """
    return a move in all possible moves that generate
    the highest winning possibility
    """
    curr = Tree(game)
    listl = [curr]
    while listl != []:
        check = listl.pop()
        check_state = check.game.current_state
        cur = check_state.get_current_player_name()
        if cur == 'p1':
            other = 'p2'
        else:
            other = 'p1'
        if check.game.is_over(check.game.current_state):
            if check.game.is_winner(cur):
                check.score = check_state.WIN
            elif check.game.is_winner(other):
                check.score = check_state.LOSE
            else:
                check.score = check_state.DRAW
        elif check.children != []:
            check.score = max([-x.score for x in check.children])
        elif check.score is None:
            listl.append(check)
            for x in check.game.current_state.get_possible_moves():
                new_game = copy.deepcopy(check.game)
                new_game.current_state = check.game.current_state.make_move(x)
                check.children.append(Tree(new_game))
            for child in check.children:
                listl.append(child)
    move = curr.game.current_state.get_possible_moves()
    maxi = 1
    g_move = 0
    for i in range(len(move)):
        if curr.children[i].score < maxi:
            maxi = curr.children[i].score
            g_move = i
    return move[g_move]


if __name__ == "__main__":
    from python_ta import check_all

    check_all(config="a2_pyta.txt")
