import random
class Rect():
    # a rectangle on the map. used to characterize a room.
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        if isinstance(w, list):
            wi = random.randint(w[0], w[1])
            self.x2 = x + wi
        else:
            self.x2 = x + w
        if isinstance(h, list):
            hi = random.randint(h[0], h[1])
            self.y2 = y + hi
        else:
            self.y2 = y + h

    def center(self):
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return (center_x, center_y)

    def intersect(self, other):
        # returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)
