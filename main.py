from game import Entity
from game import Player
x = Entity(10, 20, False, 100, "monster")
y = Player(0, 0, False, 100, "Player", "Tom")
print(x.dead)
print(x.health)
y.attack(20, x)
print(x.health)
