from dice import Dice
class Player:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.location = 0
    
    def get_location(self):
        return self.location
    
    def set_location(self, loc):
        self.location = loc
        print(f'{self.name} is at location {loc}')

        