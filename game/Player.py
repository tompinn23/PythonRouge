from . import constants
from . import Entity

class Player(Entity):
    def __init__(self, x, y, dead, health, char, entityType, name):
        super().__init__(x, y, dead, health, char, entityType)
        self.name = name

