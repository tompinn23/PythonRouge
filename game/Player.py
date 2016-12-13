from . import constants
from . import Entity

class Player(Entity):
    def __init__(self, x, y, dead, health, entityType, name):
        super().__init__(x, y, dead, health, entityType)
        self.name = name
