import sys
import logging
sys.path.append("../")
from bearlibterminal import terminal
from game import Rect
from random import randint
import random

floor = terminal.color_from_argb(100, 30, 40, 38)
floor_lit = terminal.color_from_argb(100, 173, 173, 161)
wall = terminal.color_from_argb(100, 38, 28, 61)
wall_lit = terminal.color_from_argb(100, 52, 39, 84)
_octants = ((1, 0, 0, 1),
            (0, 1, 1, 0),
            (0, -1, 1, 0),
            (-1, 0, 0, 1),
            (-1, 0, 0, -1),
            (0, -1, -1, 0),
            (0, 1, -1, 0),
            (1, 0, 0, -1))
features = ["room", "h_tunnel", "v_tunnel"]
compass = ["N", "E", "S", "W"]


class Map():
    # A game map
    def __init__(self, map_width, map_height, map_file=None):
        mult = [
            [1, 0, 0, -1, -1, 0, 0, 1],
            [0, 1, -1, 0, 0, -1, 1, 0],
            [0, 1, 1, 0, 0, -1, -1, 0],
            [1, 0, 0, 1, -1, 0, 0, -1]
        ]
        self.mult = mult
        self.map_width = map_width
        self.map_height = map_height
        if map_file is None:
            game_map = [[Tile(True) for y in range(map_height)]
                        for x in range(map_width)]
            for x in range(map_width):
                game_map[x][0].blocked = True
                game_map[x][0].block_sight = True
                game_map[x][map_height - 1].blocked = True
                game_map[x][map_height - 1].block_sight = True
            for y in range(map_height):
                game_map[0][y].blocked = True
                game_map[0][y].block_sight = True
                game_map[map_width - 1][y].blocked = True
                game_map[map_width - 1][y].block_sight = True

        else:
            game_map = map_file
        self.game_map = game_map

    def create_room(self, room):

        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.game_map[x][y].blocked = False
                self.game_map[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.game_map[x][y].blocked = False
            self.game_map[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.game_map[x][y].blocked = False
            self.game_map[x][y].block_sight = False

    def generate_dungeon(self, max_rooms):
        initial_room = Rect(self.map_width // 2, self.map_height //
                            2, randint(0, 20), randint(0, 20))
        self.create_room(initial_room)
        rooms = 0
        while rooms <= max_rooms:
            direction = random.choice(compass)
            feature = random.choice(features)
            if direction == "N":
                center_x, center_y = initial_room.center()
                if feature == "room":
                    new_room = Rect(room.x1, center_y,
                                    randint(0, 20), randint(0, 20))
                    if new_room.x1 < 0
                    or new_room.x2 < 0
                    or new_room.y1 < 0
                    or new_room.y2 < 0
                    or new_room.x1 >= self.map_width
                    or new_room.x2 >= self.map_width
                    or new_room.y1 >= self.map_height
                    or new_room.y2 >= self.map_height:
                        pass
                    else:
                        if not new_room.intersect(initial_room):
                            self.create_room(new_room)
                            rooms += 1

    def render_map(self):
        for y in range(self.map_height):
            for x in range(self.map_width):
                terminal.layer(0)
                if self.game_map[x][y].blocked is True:
                    if self.game_map[x][y].lit:
                        terminal.bkcolor(wall_lit)
                        terminal.put(x, y, ' ')
                    else:
                        terminal.bkcolor(wall)
                        terminal.put(x, y, ' ')
                else:
                    if self.game_map[x][y].lit:
                        terminal.bkcolor(floor_lit)
                        terminal.put(x, y, ' ')
                    else:
                        terminal.bkcolor(floor)
                        terminal.put(x, y, ' ')

    def draw_player_background(self, x, y):
        terminal.layer(0)
        terminal.bkcolor(floor_lit)
        terminal.put(x, y, ' ')

    def blocked(self, x, y):
        eturn(x < 0 or y < 0 or x >= self.map_width
              or y >= self.map_height or self.game_map[x][y].blocked)

    def lit(self, x, y):
        return self.game_map[x][y].lit is True

    def set_lit(self, x, y):
        if 0 <= x < self.map_width and 0 <= y < self.map_height:
            self.game_map[x][y].lit = True

    def _cast_light(self, cx, cy, row, start, end, radius, xx, xy, yx, yy, id):
        "Recursive lightcasting function"
        if start < end:
            return
        radius_squared = radius * radius
        for j in range(row, radius + 1):
            dx, dy = -j - 1, - j
            blocked = False
            while dx <= 0:
                dx += 1
                # Translate the dx, dy coordinates into map coordinates:
                X, Y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
                # l_slope and r_slope store the slopes of the left and right
                # extremities of the square we're considering:
                l_slope, r_slope = (dx - 0.5) / \
                    (dy + 0.5), (dx + 0.5) / (dy - 0.5)
                if start < r_slope:
                    continue
                elif end > l_slope:
                    break
                else:
                    # Our light beam is touching this square; light it:
                    if dx * dx + dy * dy < radius_squared:
                        self.set_lit(X, Y)
                    if blocked:
                        # we're scanning a row of blocked squares:
                        if self.blocked(X, Y):
                            new_start = r_slope
                            continue
                        else:
                            blocked = False
                            start = new_start
                    else:
                        if self.blocked(X, Y) and j < radius:
                            # This is a blocking square, start a child scan:
                            blocked = True
                            self._cast_light(cx, cy, j + 1, start, l_slope,
                                             radius, xx, xy, yx, yy, id + 1)
                            new_start = r_slope
            # Row is scanned; do next row unless last square was blocked:
            if blocked:
                break

    def do_fov(self, x, y, radius):
        "Calculate lit squares from the given location and radius"
        # do not use x and y for iterating overrides player x and y
        for j in range(self.map_width):
            for i in range(self.map_height):
                self.game_map[j][i].lit = False
        for oct in range(8):
            self._cast_light(x, y, 1, 1.0, 0.0, radius,
                             self.mult[0][oct], self.mult[1][oct],
                             self.mult[2][oct], self.mult[3][oct], 0)


class Tile():
    # a tile of the map and its properties
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        # all tiles start unexplored
        self.explored = False
        self.lit = False

        # by default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight
