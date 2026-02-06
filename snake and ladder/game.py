from collections import deque
from board import Board
from dice import Dice
from player import Player

class Game:
    def __init__(self, board: Board, dice: Dice):
        self.board = board
        self.dice = dice
        self.palyers = deque()
        self.winner = []

    def add_palyer(self, player: Player):
        self.palyers.append(player)

    def check_snack_or_ladder(self, player, pos):
        jumpers = self.board.get_jumpers()
        for jumper in jumpers:
            if jumper.start == pos:
                return jumper.apply(player)
        
        return pos


    def play(self):
        while(len(self.palyers) > 1):
            player = self.palyers.popleft()
            jump = self.dice.roll()
            reach = player.get_location() + jump
            if reach > self.board.size:
                self.add_palyer(player)
                print(f"{player.name} can't goto {reach} try next time")
                continue
            elif reach == self.board.size:
                print(f"{player.name} won the game at position {len(self.winner)+1}")
                self.winner.append(player.name)
            else:
                final_location = self.check_snack_or_ladder(player, reach)
                player.set_location(final_location)
                self.add_palyer(player)

        self.winner.append(self.palyers.pop().name)
        for rank, name in enumerate(self.winner):
            print(f"{name} at rank {rank+1}")