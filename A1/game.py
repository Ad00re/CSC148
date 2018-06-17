"""
This File contain a superclass Game and 2 cubclasses Chop and SubS
"""
from state import State, ChopState, SubState


class Game:
    """
    a object that include current state, instruction and info for next player
    of a game
    """
    def __init__(self, is_p1_turn: bool)->None:
        self.is_p1_turn = is_p1_turn
        self.current_state = State([], '')
        self.instruction = '\n'

    def __str__(self)-> str:
        """
        return the string representation of the State
        >>> game = Chop(True)
        >>> game.current_state.current_state = [0,0,1,1]
        >>> print(game)
        0011p1
        >>> game = Chop(False)
        >>> game.current_state.current_state = [1,1,1,1]
        >>> print(game)
        1111p2
        """
        rt = ''
        for item in self.current_state.current_state:
            rt += str(item)
        if self.is_p1_turn:
            rt += 'p1'
        else:
            rt += 'p2'
        return rt

    def __eq__(self, other)->bool:
        return type(self) == type(other) and \
               self.current_state == other.current_state and \
               self.is_p1_turn == other.is_p1_turn

    def is_over(self, curr)->bool:
        """
        return a boolean to show if the current game is over or not
        >>> sta = Chop(True)
        >>> curr = ChopState([1,1,0,0],'p1')
        >>> sta.is_over(curr)
        True
        """
        return curr.get_possible_moves() == []

    def get_instructions(self)->str:
        """
        return the instrution for the game
        >>> sta = Chop(True)
        >>> sta.get_instructions()
        'Two player start with one for each hand, add \
        it self to the other player hand. Game end when \
        one people has two zero.'
        """
        return self.instruction

    def is_winner(self, check: str)->bool:
        """
        check if the input player is the winner under the current situation.
        """
        raise NotImplementedError("Override this!")

    def str_to_move(self, move: str)->str:
        """
        turn a user input to a move which is similar to elements
        in possible_move
        """
        return move


class Chop(Game):
    """
    object include the current state, instruction, and next player
    of game chopstick
    """
    def __init__(self, is_p1_turn: bool) -> None:
        """
        >>>
        """
        Game.__init__(self, is_p1_turn)
        if is_p1_turn:
            player = 'p1'
        else:
            player = 'p2'
        self.current_state = ChopState([1, 1, 1, 1], player)
        self.instruction = '''Two player start with one for each hand, add 
        it self to the other player hand. Game end when
        one people has two zero.'''

    def str_to_move(self, move: str) -> str:
        """
        return the move that user input
        >>> move = 'rl'
        >>> game = Chop(True)
        >>> game.str_to_move(move)
        'RL'
        >>> move = 'Rl'
        >>> game = Chop(True)
        >>> game.str_to_move(move)
        'RL'
        """
        move = move.upper()
        return move

    def is_winner(self, check: str) -> bool:
        """
        return if the input player is the winner
        >>> game = Chop(True)
        >>> game.current_state.current_state = [0,0,1,1]
        >>> game.is_p1_turn = False
        >>> game.is_winner('p1')
        False
        >>> game = Chop(False)
        >>> game.current_state.current_state = [1,1,1,1]
        >>> game.is_p1_turnr = True
        >>> game.is_winner('p2')
        False
        """
        if self.is_over(self.current_state):
            if check == 'p1':
                if self.is_p1_turn:
                    return True
            if check == 'p2':
                if not self.is_p1_turn:
                    return True
        return False


class Sub(Game):
    """
    A game that ...
    """
    def __init__(self, is_p1_turn: bool) -> None:
        Game.__init__(self, is_p1_turn)
        self.instruction = '''suctrack number from the starting value,
        once reach zero, game ended.'''
        if is_p1_turn:
            player = 'p1'
        else:
            player = 'p2'
        score = int(input('Input a random positive integer to start:'))
        self.current_state = SubState([score], player)

    def is_winner(self, check: str)->bool:
        """
        check if the input player is the winner under the current situation.
        """
        if self.is_over(self.current_state):
            if (self.current_state.player == 'p2' and check == 'p1') or \
                    (self.current_state.player == 'p1' and check == 'p2'):
                return True
        return False


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config="a1_pyta.txt")
