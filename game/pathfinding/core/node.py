# -*- coding: utf-8 -*-
class Node(object):
    """
    basic node, saves X and Y coordinates on some grid and determine if 
    it is walkable.
    """
    def __init__(self, x=0, y=0, walkable=True):
        # Coordinates
        self.x = x
        self.y = y

        # Whether this node can be walked through.
        self.walkable = walkable

        # values used in the finder
        
        # cost from this node to the goal
        self.h = 0.0
        
        # cost from the start node to this node
        self.g = 0.0
        
        # distance from start to this point (f = g + h )
        self.f = 0.0
        
        self.opened = 0
        self.closed = False
        
        # used for backtracking to the start point
        self.parent = None

    def __lt__(self, other):
        """
        nodes are sorted by f value (see a_star.py)

        :param other: compare Node
        :return:
        """
        return self.f < other.f