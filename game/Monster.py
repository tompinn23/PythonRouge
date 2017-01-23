from . import constants
from game.Entity import Entity
from game.pathfinding.core.diagonal_movement import DiagonalMovement
from game.pathfinding.core.grid import Grid
from game.pathfinding.finder.a_star import AStarFinder

finder = AStarFinder(diagonal_movement=DiagonalMovement.never)

class Monster(Entity):
    def __init__(self, x, y, dead, health, char, entityType):
        super().__init__(x, y, dead, health, char, entityType)

    def calcMove(self, grid, startx, starty, endx, endy):
        path, runs, finder.find_path(start, end, grid)
        return path

    def makeMove(self, path):
        for move in path:
            self.x = move[0]
            self.y = move[1]
        
        
        
        
