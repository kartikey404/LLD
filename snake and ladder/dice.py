import random

class Dice:
    def __init__(self, number=1):
        self.number = number

    def roll(self):
        total = 0
        for _ in range(self.number):
            total += random.randint(1, 6)
        return total
