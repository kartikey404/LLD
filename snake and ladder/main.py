from board import Board
from dice import Dice
from game import Game
from jumper import Snake, Ladder
from player import Player

if __name__=="__main__":

    board = Board()
    dice = Dice()
    board.add_jumper(Snake(98, 45))
    board.add_jumper(Snake(56, 13))
    board.add_jumper(Ladder(41, 92))
    board.add_jumper(Ladder(15, 74))
    game = Game(board=board, dice=dice)
    counter = 0
    while True:
        name = input("Enter player name (or just enter to start): ").strip()
        if name == "":
            break
        counter += 1
        game.add_palyer(Player(name, counter))

    game.play()
    print("game finish! thankyou for paying")
