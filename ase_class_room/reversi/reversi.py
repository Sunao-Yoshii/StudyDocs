#!/bin/python

"""
this program require python 3.6+
"""


class ReversiBoard:
    STONE_WHITE = 'W'
    STONE_BLACK = 'B'
    BLANK = ' '

    """
    Define game board.
    """
    def __init__(self):
        self.__board_state = [[' ' for i in range(8)] for n in range(8)]
        self.__board_state[3][3] = ReversiBoard.STONE_BLACK
        self.__board_state[4][4] = ReversiBoard.STONE_BLACK
        self.__board_state[3][4] = ReversiBoard.STONE_WHITE
        self.__board_state[4][3] = ReversiBoard.STONE_WHITE
    
    def __is_able2put(self, x, y, color):
        if self.__board_state[y][x] != ReversiBoard.BLANK:
            return False
                
        return self.vector(1, 0, x + 1, y, True, color) or \
            self.vector(0, 1, x    , y + 1, True, color) or \
            self.vector(1, 1, x + 1, y + 1, True, color) or \
            self.vector(-1, 0 , x - 1, y    , True, color) or \
            self.vector(0, -1 , x    , y - 1, True, color) or \
            self.vector(-1, -1, x - 1, y - 1, True, color) or \
            self.vector(1, -1, x + 1, y - 1, True, color) or \
            self.vector(-1, 1, x - 1, y + 1, True, color)
    
    def vector(self, vx, vy, cx, cy, is_fst, color):
        if cx < 0 or cy < 0 or cx >= 8 or cy >= 8:
            return False
        if self.__board_state[cy][cx] == ReversiBoard.BLANK:
            return False
        if is_fst:
            if self.__board_state[cy][cx] == color:
                return False
            else:
                return self.vector(vx, vy, cx + vx, cy + vy, False, color)
        else:
            if self.__board_state[cy][cx] == color:
                return True
            else:
                return False
    
    def is_game_end(self):
        return len(self.able_to_puts(ReversiBoard.STONE_BLACK)) == 0 and len(self.able_to_puts(ReversiBoard.STONE_WHITE)) == 0
    
    def count_stones(self):
        blacks = 0
        whites = 0
        for r in self.__board_state:
            for c in r:
                if c == ReversiBoard.STONE_BLACK:
                    blacks += 1
                elif c == ReversiBoard.STONE_WHITE:
                    whites += 1
        return (blacks, whites)

    def is_win(self, color):
        if self.is_game_end():
            blacks = 0
            whites = 0
            for r in self.__board_state:
                for c in r:
                    if c == ReversiBoard.STONE_BLACK:
                        blacks += 1
                    elif c == ReversiBoard.STONE_WHITE:
                        whites += 1
            is_black_win = blacks > whites
            is_white_win = whites > blacks
            if is_black_win and color == ReversiBoard.STONE_BLACK:
                return True
            elif is_white_win and color == ReversiBoard.STONE_WHITE:
                return True
        return False
    
    def is_draw(self):
        if self.is_game_end():
            blacks = 0
            whites = 0
            for r in self.__board_state:
                for c in r:
                    if c == ReversiBoard.STONE_BLACK:
                        blacks += 1
                    elif c == ReversiBoard.STONE_WHITE:
                        whites += 1
            return blacks == whites
        return False

    def put_stone(self, color, x, y):
        def reverse(vx, vy, cx, cy):
            if cx < 0 or cy < 0 or cx >= 8 or cy >= 8:
                return
            if self.__board_state[cy][cx] == color:
                return
            elif self.__board_state[cy][cx] == ReversiBoard.BLANK:
                return
            self.__board_state[cy][cx] = color
            reverse(vx, vy, cx + vx, cy + vy)
        
        self.__board_state[y][x] = color

        if self.vector(1, 0, x + 1, y, True, color):
            reverse(1, 0, x + 1, y)
        if self.vector(0, 1, x, y + 1, True, color):
            reverse(0, 1, x, y + 1)
        if self.vector(1, 1, x + 1, y + 1, True, color):
            reverse(1, 1, x + 1, y + 1)

        if self.vector(-1, 0, x - 1, y, True, color):
            reverse(-1, 0, x - 1, y)
        if self.vector(0, -1, x, y - 1, True, color):
            reverse(0, -1, x, y - 1)
        if self.vector(-1, -1, x - 1, y - 1, True, color):
            reverse(-1, -1, x - 1, y - 1)
    
    def able_to_puts(self, color):
        """
        detect replaceable positions.
        """
        positions = []
        for y in range(len(self.__board_state)):
            for x in range(len(self.__board_state[y])):
                if self.__is_able2put(x, y, color):
                    positions.append((x, y))
        return positions
    
    def show(self):
        """
        Render bord status.
        """
        print(self.to_string())
    
    def to_string(self):
        ylength = len(self.__board_state)
        id_list = zip(range(ylength), self.__board_state)

        rendered_board = "  0 1 2 3 4 5 6 7\n"
        rendered_board += "\n".join([f'{n} ' + " ".join(row) for n, row in id_list])
        return rendered_board


class Player:
    def __init__(self, board, color):
        self.__board = board
        self.__color = color

    def put(self):
        ables = self.__board.able_to_puts(self.__color)
        print(ables)
        print(f'Input index({self.__color}):')
        position_id = int(input('>>'))
        x, y = ables[position_id]
        self.__board.put_stone(self.__color, x, y)


if __name__ == "__main__":
    board = ReversiBoard()
    player1 = Player(board, ReversiBoard.STONE_BLACK)
    player2 = Player(board, ReversiBoard.STONE_WHITE)
    players = [player1, player2]
    turn = 0
    
    while not board.is_game_end():
        board.show()
        pl = players[turn % 2]
        turn += 1
        pl.put()
    
    if board.is_draw():
        print('Draw')
    elif board.is_win(ReversiBoard.STONE_BLACK):
        print('Winner is Black')
    else:
        print('Winner is white')