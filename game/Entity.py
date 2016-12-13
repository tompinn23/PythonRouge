from . import constants

class Entity():
    def __init__(self, x, y, dead, health, entityType):
        self.x = x
        self.y = y
        self.dead = dead
        self.health = health
    def onAttack(self, damage):
        if damage >= self.health:
            self.dead = True
        else:
            self.health = self.health - damage

    def attack(self, attackPower, entity):
        entity.onAttack(attackPower)

    def move(self, dy, dx):
        self.x += dx
        self.y += dy
        
    
        
        
        
        
        
        
