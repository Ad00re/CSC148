"""
File Contain State, ChopState, SubState
"""
from typing import List, Any
import math


class State:
    """
    The type for the current_state under type Game
    Including a list and the player name
    """
    def __init__(self, score: List[int], player: str)->None:
        """
        This method should not be directly called
        """
        self.current_state = score
        self.player = player

    def __str__(self)->str:
        """
        This method should not be directly called
        """
        raise NotImplementedError("Override this!")

    def get_possible_moves(self)-> List:
        """
        This method should not be directly called
        """
        raise NotImplementedError("Override this!")

    def is_valid_move(self, move: str)-> bool:
        """
        return a boolean to see if the move is valid or not
        >>> move = 'RL'
        >>> sta = ChopState([1,1,1,1],'p1')
        >>> sta.is_valid_move(move)
        True
        >>> move = '25'
        >>> sta = SubState([24],'p1')
        >>> sta.is_valid_move(move)
        False
        """
        return move in self.get_possible_moves()

    def make_move(self, move: str)-> None:
        """
        This method should not be directly called
        """
        raise NotImplementedError("Override this!")

    def get_current_player_name(self)->str:
        """
        return the current player name
        >>> sta = State([25],'p1')
        >>> sta.get_current_player_name()
        'p1'
        >>> sta = State([1,1,0,0],'p1')
        >>> sta.get_current_player_name()
        'p1'
        """
        return self.player

    def __eq__(self, other: Any)->bool:
        """
        return True is and only if the curent player and current state are same
        >>> sta1 = State([25],'p1')
        >>> sta2 = State([25],'p1')
        >>> sta1 == sta2
        True
        >>> sta1 = State([1,1,0,0],'p1')
        >>> sta2 = State([0,0,1,1],'p1')
        >>> sta1 == sta2
        False
        """
        boo = False
        if type(self) == type(other):
            if self.current_state == other.current_state \
                    and self.player == other.player:
                boo = True
        return boo


class ChopState(State):
    """
    the current_state for a chopstick game
    """
    def __str__(self) -> str:
        """
        Print out the current state for the gamw
        >>> sta = ChopState([1,1,1,1],'p1')
        >>> print(sta)
        ...1-1...1-1...
        """
        li = self.current_state
        out = '...' + str(li[0]) + '-' + str(li[1]) + '...' + str(li[2]) + '-' \
              + str(li[3]) + '...'
        return out

    def get_possible_moves(self) -> List:
        """
        return a list contain of all posible moves
        >>> sta = ChopState([1,1,1,1],'p1')
        >>> sta.get_possible_moves()
        ['LL', 'LR', 'RL', 'RR']
        >>> sta = ChopState([1,1,1,0],'p1')
        >>> sta.get_possible_moves()
        ['LL', 'RL']
        """
        cur = self.current_state
        hand = 'LR'
        poss = []
        for i in range(2):
            for j in range(2, 4):
                if self.player == 'p1' and cur[i] != 0 and cur[j] != 0:
                    ad = hand[i % 2] + hand[j % 2]
                    poss.append(ad)
                elif self.player == 'p2' and cur[i] != 0 and cur[j] != 0:
                    ad = hand[j % 2] + hand[i % 2]
                    poss.append(ad)
        return poss

    def make_move(self, move: str) -> State:
        """
        return a new state after the move applied
        >>> sta = ChopState([1, 1, 1, 1],'p1')
        >>> nu = sta.make_move('RL')
        >>> nu.current_state
        [1, 1, 2, 1]
        >>> nu.player
        'p2'
        >>> sta = ChopState([1, 1, 4, 1],'p1')
        >>> nu = sta.make_move('RL')
        >>> nu.current_state
        [1, 1, 0, 1]
        >>> nu.player
        'p2'
        """
        move = move.upper()
        pl = self.player
        te = []
        for item in self.current_state:
            te.append(item)

        if pl == 'p1':
            pl = 'p2'
            if move[0] == 'L' and move[1] == 'L':
                te[2] = (te[2]+te[0]) % 5
            elif move[0] == 'L' and move[1] == 'R':
                te[3] = (te[3] + te[0]) % 5
            elif move[0] == 'R' and move[1] == 'L':
                te[2] = (te[2] + te[1]) % 5
            elif move[0] == 'R' and move[1] == 'R':
                te[3] = (te[3] + te[1]) % 5
        elif pl == 'p2':
            pl = 'p1'
            if move[0] == 'L' and move[1] == 'L':
                te[0] = (te[0] + te[2]) % 5
            elif move[0] == 'L' and move[1] == 'R':
                te[1] = (te[1] + te[2]) % 5
            elif move[0] == 'R' and move[1] == 'L':
                te[0] = (te[0] + te[3]) % 5
            elif move[0] == 'R' and move[1] == 'R':
                te[1] = (te[1] + te[3]) % 5
        f = ChopState(te, pl)
        return f


class SubState(State):
    """
    The current state of substract square game
    """
    def __str__(self) -> str:
        """
        Return the current number for the game
        >>> sta = SubState([25], 'p1')
        >>> print(sta)
        (25)
        """

        return "" '(' + str(self.current_state[0]) + ')'""

    def get_possible_moves(self) -> List:
        """
        return a list contain all possible moves
        >>> sta = SubState([25], 'p1')
        >>> sta.get_possible_moves()
        ['1', '4', '9', '16', '25']
        >>> sta = SubState([8], 'p1')
        >>> sta.get_possible_moves()
        ['1', '4']
        """
        cur = self.current_state[0]
        poss = []
        maxi = int(math.floor(cur ** 0.5))
        for i in range(maxi+1):
            poss.append(str(i**2))
        poss.pop(0)
        return poss

    def make_move(self, move: str) -> State:
        """
        return the state after the change has been made
        >>> sta = SubState([25],'p1')
        >>> nu = sta.make_move('16')
        >>> nu.current_state
        [9]
        >>> nu.player
        'p2'
        >>> sta = SubState([20],'p1')
        >>> nu = sta.make_move('9')
        >>> nu.current_state
        [11]
        >>> nu.player
        'p2'
        """
        sc = self.current_state[0]
        pl = self.player
        if pl == 'p1':
            pl = 'p2'
        else:
            pl = 'p1'
        sc -= int(move)
        f = SubState([sc], pl)
        return f


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config="a1_pyta.txt")
