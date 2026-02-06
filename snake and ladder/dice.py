import random


class Dice:
    def __init__(self, number=1):
        self.number = number

    def roll(self):
        return random.randint(1*self.number, 6*self.number)