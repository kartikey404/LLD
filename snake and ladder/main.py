from board import Board
from dice import Dice
from game import Game
from jumper import Snake, Ladder
from player import Player


def read_int(prompt, default=None):
    while True:
        raw = input(prompt).strip()
        if raw == "" and default is not None:
            return default
        try:
            return int(raw)
        except ValueError:
            print("Please enter a valid number.")


if __name__=="__main__":

    board_size = read_int("Enter board size (default 100): ", default=100)
    board = Board(size=board_size)
    dice = Dice()

    print("Add jumpers: type 'snake' or 'ladder' (press Enter to finish).")
    while True:
        kind = input("Jumper type: ").strip().lower()
        if kind == "":
            break
        if kind not in {"snake", "ladder"}:
            print("Type must be 'snake' or 'ladder'.")
            continue

        start = read_int("Start position: ")
        end = read_int("End position: ")

        if start < 1 or start > board.size or end < 1 or end > board.size:
            print("Start and end must be within the board size.")
            continue
        if start == end:
            print("Start and end must be different.")
            continue
        if kind == "snake" and end >= start:
            print("A snake must go down (end < start).")
            continue
        if kind == "ladder" and end <= start:
            print("A ladder must go up (end > start).")
            continue

        if kind == "snake":
            board.add_jumper(Snake(start, end))
        else:
            board.add_jumper(Ladder(start, end))

    game = Game(board=board, dice=dice)
    counter = 0
    while True:
        name = input("Enter player name (or just enter to start): ").strip()
        if name == "":
            break
        counter += 1
        game.add_player(Player(name, counter))

    if counter < 2:
        print("Add at least two players to start the game.")
    else:
        game.play()
        print("Game finished. Thank you for playing.")
