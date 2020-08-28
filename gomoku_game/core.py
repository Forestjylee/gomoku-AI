from pprint import pprint
from copy import deepcopy
from collections import deque


class Gomoku(object):

    EMPTY = 0
    WHITE = 1
    BLACK = 2

    def __init__(self, rows, cols, win_pieces=5):
        self.__rows = rows
        self.__cols = cols
        self.__win_pieces = win_pieces
        self.__board = self.get_empty_board(rows, cols)

        self.__records = deque()

    def get_rows(self):
        return self.__rows
    
    def get_cols(self):
        return self.__cols

    def get_board(self):
        return deepcopy(self.__board)

    def print_board(self):
        pprint(self.__board)

    def print_records(self):
        for index, record in enumerate(self.__records):
            piece = "WHITE" if record[2] == self.WHITE else "BLACK"
            print(f"step {index}: {piece} drop piece at <{record[0]}, {record[1]}>")

    def get_empty_board(self, rows, cols):
        empty_board = []
        v = [self.EMPTY] * rows
        for col in range(cols):
            empty_board.append(deepcopy(v))
        return empty_board
    
    def drop_piece(self, row, col, piece):
        if self.__board[row][col] == 0:
            self.__board[row][col] = piece
            self.__records.append((row, col, piece))
            return True
        else:
            return False

    def roll_back(self, steps=1):
        for i in range(steps):
            row, col, piece = self.__records.pop()
            self.__board[row][col] = self.EMPTY

    def check_win(self):
        # horizontal
        for row in range(self.__rows):
            for col in range(self.__cols - self.__win_pieces + 1):
                window = self.__board[row][col:col+self.__win_pieces]
                if self.check_windows(window, self.__win_pieces, self.WHITE):
                    return self.WHITE
                if self.check_windows(window, self.__win_pieces, self.BLACK):
                    return self.BLACK
        # vertical     
        for col in range(self.__cols):
            for row in range(self.__rows-self.__win_pieces+1):
                window = []
                for i in range(row, row+self.__win_pieces):
                    window.append(self.__board[i][col])
                if self.check_windows(window, self.__win_pieces, self.WHITE):
                    return self.WHITE
                if self.check_windows(window, self.__win_pieces, self.BLACK):
                    return self.BLACK
        # positive diagonal
        for row in range(self.__rows-self.__win_pieces+1):
            for col in range(self.__cols-self.__win_pieces+1):
                window = []
                for i in range(row, row + self.__win_pieces):
                    for j in range(col, col + self.__win_pieces):
                        window.append(self.__board[i][j])
                if self.check_windows(window, self.__win_pieces, self.WHITE):
                    return self.WHITE
                if self.check_windows(window, self.__win_pieces, self.BLACK):
                    return self.BLACK
        # negative diagonal
        for col in range(self.__cols-self.__win_pieces+1):
            for row in range(self.__win_pieces-1, self.__rows):
                window = []
                for i in range(row, row - self.__win_pieces, -1):
                    for j in range(col, col + self.__win_pieces):
                        window.append(self.__board[i][j])
                if self.check_windows(window, self.__win_pieces, self.WHITE):
                    return self.WHITE
                if self.check_windows(window, self.__win_pieces, self.BLACK):
                    return self.BLACK
        return self.EMPTY

    def imitate_drop_piece(board, row, col, piece):
        if board[row][col] == 0:
            board[row][col] = piece
            return board
        else:
            return False   

    def count_windows(self, board, num_discs, piece):
        num_windows = 0
        # horizontal
        for row in range(self.__rows):
            for col in range(self.__cols - self.__win_pieces + 1):
                window = board[row][col:col+self.__win_pieces]
                if self.check_windows(window, num_discs, piece):
                    num_windows += 1
        # vertical     
        for col in range(self.__cols):
            for row in range(self.__rows-self.__win_pieces+1):
                window = []
                for i in range(row, row+self.__win_pieces):
                    window.append(board[i][col])
                if self.check_windows(window, num_discs, piece):
                    num_windows += 1
        # positive diagonal
        for row in range(self.__rows-self.__win_pieces+1):
            for col in range(self.__cols-self.__win_pieces+1):
                window = []
                for i in range(row, row + self.__win_pieces):
                    for j in range(col, col + self.__win_pieces):
                        window.append(board[i][j])
                if self.check_windows(window, num_discs, piece):
                    num_windows += 1    
        # negative diagonal
        for col in range(self.__cols-self.__win_pieces+1):
            for row in range(self.__win_pieces-1, self.__rows):
                window = []
                for i in range(row, row - self.__win_pieces, -1):
                    for j in range(col, col + self.__win_pieces):
                        window.append(board[i][j])
                if self.check_windows(window, num_discs, piece):
                    num_windows += 1
        return num_windows

    def check_windows(self, window, num_discs, piece):
        return window.count(piece) == num_discs and window.count(0) == self.__win_pieces-num_discs

    @classmethod
    def standard_game(cls):
        return cls(rows=15, cols=15, win_pieces=5)
