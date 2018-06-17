"""
a stonehenge game
"""
from typing import Any
from game import Game
from game_state import GameState


class StonehengeGame(Game):
    """
    the overall for a stonehenge game
    """
    def __init__(self, is_p1_turn: bool)-> None:
        """
        Start a new game
        """
        n = int(input("Please enter the size for stonehenge"))
        alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        alpha_list = [str(x) for x in alpha]
        size = int(n * (n + 5) / 2)
        lay = [[], [], []]
        for i in range(3):
            for j in range(n+1):
                lay[i].append(['@', 0, 0, n+1-abs(n-1-j)])
        self.current_state = StonehengeState(is_p1_turn,
                                             alpha_list[:size], n, lay)

    def get_instructions(self)->str:
        """
        get instruction
        """
        instruction = 'Stonehenge is played on a hexagonal grid formed by ' \
                      'removing the corners from a triangular grid. '
        return instruction

    def is_over(self, state: GameState)-> bool:
        """
        return True if and only if the game is over
        """
        al = (state.n + 1) * 3
        claim = []
        for i in range(3):
            for j in range(state.n + 1):
                claim.append(state.lay[i][j][0])
        a_claim = claim.count('1')
        b_claim = claim.count('2')
        return a_claim * 2 >= al or b_claim * 2 >= al

    def is_winner(self, player: str)->bool:
        """
        return True if and only if
        the the player the user is checking is the winner
        """
        if not self.is_over(self.current_state):
            return False
        claim = []
        for i in range(3):
            for j in range(self.current_state.n + 1):
                claim.append(self.current_state.lay[i][j][0])
        a_claim = claim.count('1')
        b_claim = claim.count('2')
        if player == 'p1':
            return a_claim * 2 >= (self.current_state.n + 1) * 3
        elif player == 'p2':
            return b_claim * 2 >= (self.current_state.n + 1) * 3
        return False

    def str_to_move(self, string: str)->str:
        """
        change the user's input to a valid move
        """
        string = string.upper()
        return string


class StonehengeState(GameState):
    """
    The current state for a stonehenge game
    """
    def __init__(self, is_p1_turn: bool, poss: list, n: int, lay: list)->None:
        """
        init a new game state for stonehenge
        """
        super().__init__(is_p1_turn)
        self.poss_move = poss
        self.n = n
        self.lay = lay

    def __str__(self)->str:
        """
        return the current state to the user
        """
        re = ''
        nu = []
        for item in self.poss_move:
            nu.append(item)
        re += (self.n+2) * '  ' + self.lay[1][self.n][0] + '   ' \
              + self.lay[1][self.n-1][0] + '\n'
        re += (2*self.n + 3) * ' ' + '/   /' + '\n'
        for i in range(2, self.n+2):
            neu = nu[:i]
            for x in neu:
                nu.remove(x)
            if i <= self.n:
                re += ((self.n + 1 - i) * '  ' + self.lay[0][i-2][0] + ' - ' +
                       ' - '.join(neu) + '   ' + self.lay[1][self.n - i][0])\
                      + '\n'
                re += ((2 * (self.n + 3 - i) - 1) * ' ' + '/ \\ ' * i + '/'
                       + '\n')
            else:
                re += (self.lay[0][self.n-1][0]+' - ' + ' - '.join(neu)) + '\n'
                re += ('     '+'\\ / '*(i-1)) + '\\' + '\n'
        re += '  ' + self.lay[0][self.n][0]+' - '+' - '.join(nu) \
              + '   ' + self.lay[2][self.n][0]+'\n'
        re += ' '*7 + '\\   ' * self.n + '\n'
        re += ' '*8 + '   '.join([self.lay[2][i][0] for i in range(self.n)])
        return re

    def get_possible_moves(self)->list:
        """
        return all the possible moves under the current state
        >>> a = StonehengeState(True, ['A','B','C'], 1, \
        [[['@',0,0,2],['@',0,0,1]],[['@',0,0,2],['@',0,0,1]],[['@',0,0,2],['@',0,0,1]]])
        >>> a.get_possible_moves()
        ['A', 'B', 'C']
        >>> a = StonehengeState(True, ['A','B','1'], 1, \
        [[['@',0,0,2],['@',0,0,1]],[['@',0,0,2],['@',0,0,1]],[['@',0,0,2],['@',0,0,1]]])
        >>> a.get_possible_moves()
        ['A', 'B']
        """
        al = (self.n + 1) * 3
        claim = []
        for i in range(3):
            for j in range(self.n + 1):
                claim.append(self.lay[i][j][0])
        a_claim = claim.count('1')
        b_claim = claim.count('2')
        if a_claim * 2 >= al or b_claim * 2 >= al:
            return []
        curr = []
        for item in self.poss_move:
            if item != '1' and item != '2':
                curr.append(item)
        return curr

    def make_move(self, move: Any) -> "StonehengeState":
        """
        return a new game state after a move
        >>> a = StonehengeState(True, ['A','B','C'], 1, \
        [[['@',0,0,2],['@',0,0,1]],[['@',0,0,2],['@',0,0,1]],[['@',0,0,2],['@',0,0,1]]])
        >>> b = a.make_move('A')
        >>> b.get_possible_moves()
        []
        >>> b.lay
        [[['1', 1, 0, 2], ['@', 0, 0, 1]], [['@', 0, 0, 2], ['1', 1, 0, 1]], [['1', 1, 0, 2], ['@', 0, 0, 1]]]
        """
        index = self.poss_move.index(move) + 1
        position = self.get_lay_line(index)
        if self.p1_turn:
            p1 = False
        else:
            p1 = True
        nu = []
        for i in range(len(self.poss_move)):
            if i != index-1:
                nu.append(self.poss_move[i])
            else:
                if self.p1_turn:
                    nu.append('1')
                else:
                    nu.append('2')
        new_l = [[], [], []]
        for i in range(3):
            for j in range(self.n + 1):
                if j != position[i] or self.lay[i][j][0] != '@':
                    new_l[i].append([self.lay[i][j][0], self.lay[i][j][1],
                                     self.lay[i][j][2], self.lay[i][j][3]])
                else:
                    new_l = self.make(i, j, new_l)
        return StonehengeState(p1, nu, self.n, new_l)

    def make(self, i: int, j: int, new_l: list)->Any:
        """
        a helper function for make move that change the laylines and the board
        by the number of lay line
        """
        if self.p1_turn:
            if (self.lay[i][j][1] + 1) * 2 >= self.lay[i][j][3]:

                new_l[i].append(['1', self.lay[i][j][1] + 1,
                                 self.lay[i][j][2],
                                 self.lay[i][j][3]])
            else:
                new_l[i].append([self.lay[i][j][0],
                                 self.lay[i][j][1] + 1,
                                 self.lay[i][j][2],
                                 self.lay[i][j][3]])
        else:
            if (self.lay[i][j][2] + 1) * 2 >= self.lay[i][j][3]:
                new_l[i].append(['2', self.lay[i][j][1],
                                 self.lay[i][j][2] + 1,
                                 self.lay[i][j][3]])
            else:
                new_l[i].append([self.lay[i][j][0],
                                 self.lay[i][j][1],
                                 self.lay[i][j][2] + 1,
                                 self.lay[i][j][3]])
        return new_l

    def get_lay_line(self, index: int)->list:
        """
        get the index for the lay line
        """
        ran = [0, 2, 5, 9, 14, 20]
        line = 0
        re = 0
        for i in range(1, 6):
            if index <= ran[i]:
                line = i
                re = index - ran[i - 1]
                index = 250
        if index != 250:
            line = 6
            re = index - 20
        if line == self.n + 1:
            re += 1
        lower = (self.n - line) + re
        return [line-1, self.n - re + 1, lower - 1]

    def __repr__(self)->str:
        """
        return a representation of the current state
        """
        if self.p1_turn:
            player = 'p1'
        else:
            player = 'p2'
        return 'The current player is '+player+self.__str__()

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.
        >>> a = StonehengeState(True, ['A','B','C'], 1, \
        [[['@',0,0,2],['@',0,0,1]],[['@',0,0,2],['@',0,0,1]],[['@',0,0,2],['@',0,0,1]]])
        >>> b = a.make_move('A')
        >>> b.rough_outcome()
        -1
        >>> a = StonehengeState(True, ['A','B','C'], 1, \
        [[['@',0,0,2],['@',0,0,1]],[['@',0,0,2],['@',0,0,1]],[['@',0,0,2],['@',0,0,1]]])
        >>> b = a.make_move('B')
        >>> b.rough_outcome()
        -1
        """
        if any([self.make_move(x).get_possible_moves() == []
                for x in self.get_possible_moves()]):
            return self.WIN
        elif all([any([self.make_move(x).make_move(y).get_possible_moves() == []
                       for y in self.make_move(x).get_possible_moves()])
                  for x in self.get_possible_moves()]):
            return self.LOSE
        claim = []
        for i in range(3):
            for j in range(self.n + 1):
                claim.append(self.lay[i][j][0])
        a_claim, b_claim = claim.count('1'), claim.count('2')
        if self.p1_turn:
            if a_claim * 2 >= (self.n + 1) * 3:
                return self.WIN
            elif b_claim * 2 >= (self.n + 1) * 3:
                return self.LOSE
            return (a_claim-b_claim) / (a_claim + b_claim + 1)
        if b_claim * 2 >= (self.n + 1) * 3:
            return self.WIN
        elif a_claim * 2 >= (self.n + 1) * 3:
            return self.LOSE
        return (b_claim - a_claim) / (a_claim + b_claim + 1)


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
