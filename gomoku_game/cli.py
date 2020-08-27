from core import Gomoku
from prettytable import PrettyTable


def help():
    pt = PrettyTable(["Command", "Parameters", "Description"])
    pt.add_row(["h/help", "-", "Show all commands and corresponding description."])
    pt.add_row(["s/start", "-", "Start a new game"])
    pt.add_row(["d/drop", "row, col", "Drop piece on chess board"])
    pt.add_row(["r/rollback", "-", "Rollback last piece you droped"])
    pt.add_row(["q/quit", "-", "Quit game"])
    print(pt)

def main():
    gameover = True
    while True:
        if gameover:
            g = Gomoku.standard_game()
        command = input("请输入指令>")
        if command == "h" or command == "help":
            help()
        elif command == "q" or command == "quit":
            break


if __name__ == "__main__":
    main()
