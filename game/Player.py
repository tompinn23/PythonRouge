
from game.Entity import Entity

class Player(Entity):
    def __init__(self, x, y, dead, health, char, name):
        super().__init__(x, y, dead, health, char, "Player")
        self.name = name

    def setName(self, name):
        self.name = name

    def setChar(self, char):
        self.char = char

    def getChar(self):
        return self.char

    def getPlayerData(self):
        return (self.x, self.y, self.dead, self.health, self.char, self.name)


    def setPlayerData(self, **kwargs):
        for key in kwargs:
            if key == 'x':
                self.x = kwargs[key]
            if key == 'y':
                self.y = kwargs[key]
            if key == 'dead':
                self.dead = kwargs[key]
            if key == 'health':
                self.health = kwargs[key]
            if key == 'char':
                self.char = kwargs[key]
            if key == 'name':
                self.name = kwargs[key]
