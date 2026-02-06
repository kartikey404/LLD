from jumper import Jumper
class Board:
    def __init__(self, size=100):
        self.size = size
        self.jumpers = []

    def add_jumper(self, jumper: Jumper):
        self.jumpers.append(jumper)

    def get_jumpers(self):
        return self.jumpers