import sys
sys.path.append("../")
from bearlibterminal import terminal
from . import constants


class Entity():
    def __init__(self, x, y, dead, health, char, entityType):
        self.x = x
        self.y = y
        self.dead = dead
        self.health = health
        self.char = char

    def onAttack(self, damage):
        if damage >= self.health:
            self.dead = True
        else:
            self.health = self.health - damage

    def attack(self, attackPower, entity):
        entity.onAttack(attackPower)

    def move(self, dx, dy, _map):
        if not _map[self.x + dx][self.y + dy].blocked:
            self.x += dx
            self.y += dy

    def draw(self):
        terminal.put(self.x, self.y, self.char)

    def clear(self):
        terminal.put(self.x, self.y, ' ')
