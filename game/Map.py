import sys
import logging
sys.path.append("../")
from bearlibterminal import terminal
import random
import game.newGenerator
from game.newGenerator import Tiles

floor = terminal.color_from_argb(100, 30, 40, 38)
floor_lit = terminal.color_from_argb(100, 173, 173, 161)
wall = terminal.color_from_argb(100, 97, 145, 49)
wall_lit = terminal.color_from_argb(100, 136, 181, 91)
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

    def create_h_tunnel(self, room):
        for x in range(min(room.x1, room.x2), max(room.x1, room.x2) + 1):
            self.game_map[x][room.y1].blocked = False
            self.game_map[x][room.y1].block_sight = False

    def create_v_tunnel(self, room):
        for y in range(min(room.y1, room.y2), max(room.y1, room.y2) + 1):
            self.game_map[room.x1][y].blocked = False
            self.game_map[room.x1][y].block_sight = False

    def generate_Dungeon(self, w ,h):
        aw = w / 5
        ah = h / 5
        tiles = game.newGenerator.generate(int(aw), int(ah), 5)
        for y in range(self.map_height):
            for x in range(self.map_width):
                    if tiles[(x, y)] == Tiles.FLOOR:
                        self.game_map[x][y].blocked = False
                        self.game_map[x][y].block_sight = False
                    if tiles[(x, y)] == Tiles.WALL:
                        self.game_map[x][y].blocked = True
                        self.game_map[x][y].block_sight = True
                    if tiles[(x, y)] == Tiles.EMPTY:
                        self.game_map[x][y].blocked = True
                        self.game_map[x][y].block_sight = True
                    if tiles[(x, y)] == Tiles.STAIRDOWN or tiles[(x, y)] == Tiles.STAIRUP:
                        self.game_map[x][y].blocked = False
                        self.game_map[x][y].block_sight = False


    def findPlayerLoc(self):
        playerLoc = False
        while not playerLoc:
            for x in range(self.map_width):
                for y in range(self.map_height):
                    if self.game_map[x][y].blocked is False:
                        return x, y
                        playerLoc = True
                        break

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

    def blocked(self, x, y):
        return(x < 0 or y < 0 or x >= self.map_width
               or y >= self.map_height or self.game_map[x][y].blocked)

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
