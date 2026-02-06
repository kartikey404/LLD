from player import Player
class Jumper:
    def __init__(self, from_loc, to_loc):
        self.start = from_loc
        self.end = to_loc

    def goto(self):
        return self.end
    
class Snake(Jumper):

    def apply(self, player: Player):
        print(f"{player.name} got bitten at {self.start} falling to {self.end}")
        return self.goto()

class Ladder(Jumper):

    def apply(self, player: Player):
        print(f"{player.name} fount a ladder rise up to {self.end}")
        return self.goto()