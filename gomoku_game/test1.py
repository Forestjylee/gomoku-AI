from core import Gomoku


if __name__ == "__main__":
    g = Gomoku.standard_game()
    bo = g.get_board()
    g.drop_piece(0, 0, g.WHITE)
    g.drop_piece(0, 1, g.BLACK)
    g.drop_piece(0, 2, g.BLACK)
    g.drop_piece(0, 3, g.BLACK)
    g.drop_piece(0, 4, g.BLACK)
    # g.drop_piece(0, 5, g.BLACK)
    g.print_board()
    g.print_records()
    g.roll_back()
    g.print_board()
    g.print_records()
    print(g.check_win())
