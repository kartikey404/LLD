from collections import deque
from board import Board
from dice import Dice
from player import Player

class Game:
    def __init__(self, board: Board, dice: Dice):
        self.board = board
        self.dice = dice
        self.players = deque()
        self.winner = []

    def add_player(self, player: Player):
        self.players.append(player)

    def check_snake_or_ladder(self, player: Player, pos: int) -> int:
        jumpers = self.board.get_jumpers()
        for jumper in jumpers:
            if jumper.start == pos:
                return jumper.apply(player)

        return pos

    def play(self):
        while len(self.players) > 1:
            player = self.players.popleft()
            jump = self.dice.roll()
            reach = player.get_location() + jump

            if reach > self.board.size:
                self.add_player(player)
                print(f"{player.name} can't go to {reach}, try next time")
                continue

            if reach == self.board.size:
                print(f"{player.name} won the game at position {len(self.winner) + 1}")
                self.winner.append(player.name)
                continue

            final_location = self.check_snake_or_ladder(player, reach)
            player.set_location(final_location)
            self.add_player(player)

        if len(self.players) == 1:
            last_player = self.players.pop()
            if last_player.name not in self.winner:
                self.winner.append(last_player.name)

        if len(self.winner) == 0:
            print("No winners. Add at least two players to play.")
            return

        for rank, name in enumerate(self.winner):
            print(f"{name} at rank {rank + 1}")
