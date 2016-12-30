import sys
import logging
sys.path.append("../")
from bearlibterminal import terminal
from game import features
from game import generator
from game import dungeonGenerator
import random


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

    # def generate_dungeon(self, w ,h):
    #     dungeon = generator.Generator(w, h)
    #     dungeon.gen_level()
    #     tiles = dungeon.gen_tiles_level()
    #     y = 0
    #     for row in tiles:
    #         cur = list(row)
    #         for x in range(len(cur)):
    #             if cur[x] == '0' or cur[x] == '2':
    #                 self.game_map[x][y].blocked = True
    #                 self.game_map[x][y].block_sight = True
    #             if cur[x] == '1':
    #                 self.game_map[x][y].blocked = False
    #                 self.game_map[x][y].block_sight = False
    #         y += 1
    def generate_dungeon(self, w, h):
        dm = dungeonGenerator.dungeonGenerator(w, h)
        dm.generateCaves(40, 4)
        # clear away small islands
        unconnected = dm.findUnconnectedAreas()
        for area in unconnected:
            if len(area) < 35:
                for x, y in area:
                    dm.grid[x][y] = EMPTY
        # generate rooms and corridors
        dm.placeRandomRooms(5, 9, 1, 1, 2000)
        x, y = dm.findEmptySpace(3)
        while x:
            dm.generateCorridors('l', x, y)
            x, y = dm.findEmptySpace(3)
        # join it all together
        dm.connectAllRooms(0)
        unconnected = dm.findUnconnectedAreas()
        dm.joinUnconnectedAreas(unconnected)
        dm.pruneDeadends(70)

        for x in range(self.map_width):
            for y in range(self.map_height):
                if dm.grid[x][y] == EMPTY or dm.grid[x][y] == WALL or dm.grid[x][y] == OBSTACLE:
                    self.game_map[x][y].blocked = True
                    self.game_map[x][y].block_sight = True
            if  dm.grid[x][y] == FLOOR or dm.grid[x][y] == CORRIDOR or dm.grid[x][y] == DOOR or dm.grid[x][y] == CAVE:
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





    # def generate_dungeon(self, max_rooms):
    #     width = self.map_width // 2
    #     height = self.map_height // 2
    #     initial_room = features.Room(width, height, [0, 20], [0, 20])
    #     initial_feature = initial_room
    #     self.create_room(initial_room)
    #     rooms = 0
    #     while rooms <= max_rooms:
    #         direction = random.choice(compass)
    #         if initial_feature.id == "room":
    #             center_x, center_y = initial_feature.center()
    #             if direction == "N":
    #                 new_feature = features.V_tunnel(center_x, initial_feature.y1, [
    #                                    initial_feature.y1 + 1, initial_feature.y1 + 10])
    #                 try:
    #                     self.create_v_tunnel(new_feature)
    #                 except IndexError:
    #                     pass
    #             if direction == "E":
    #                 new_feature = features.H_tunnel(initial_feature.x2, center_y, [
    #                                    initial_feature.x2 + 1, initial_feature.x2 + 10])
    #                 try:
    #                     self.create_h_tunnel(new_feature)
    #                 except IndexError:
    #                     pass
    #             if direction == "S":
    #                 new_feature = features.V_tunnel(center_x, initial_feature.y2, [
    #                                    initial_feature.y2 - 10, initial_feature.y2 - 1])
    #                 try:
    #                     self.create_v_tunnel(new_feature)
    #                 except IndexError:
    #                     pass
    #             if direction == "W":
    #                 new_feature = features.H_tunnel(initial_feature.x1, center_y, [
    #                                    initial_feature.x1 - 10, initial_feature.x1 - 1])
    #                 try:
    #                     self.create_h_tunnel(new_feature)
    #                 except IndexError:
    #                     pass
    #         if initial_feature.id == "v_tunnel" or initial_feature.id == "h_tunnel":
    #             if direction == "N":
    #                 new_feature = features.V_tunnel(center_x, initial_feature.y1, [
    #                                    initial_feature.y1 + 1, initial_feature.y1 + 10])
    #                 try:
    #                     self.create_v_tunnel(new_feature)
    #                 except IndexError:
    #                     pass
    #             if direction == "E":
    #                 new_feature = features.H_tunnel(initial_feature.x2, center_y, [
    #                                    initial_feature.x2 + 1, initial_feature.x2 + 10])
    #                 try:
    #                     self.create_h_tunnel(new_feature)
    #                 except IndexError:
    #                     pass
    #             if direction == "S":
    #                 new_feature = features.V_tunnel(center_x, initial_feature.y2, [
    #                                    initial_feature.y2 - 10, initial_feature.y2 - 1])
    #                 try:
    #                     self.create_v_tunnel(new_feature)
    #                 except IndexError:
    #                     pass
    #             if direction == "W":
    #                 new_feature = features.H_tunnel(initial_feature.x1, center_y, [
    #                                    initial_feature.x1 - 10, initial_feature.x1 - 1])
    #                 try:
    #                     self.create_h_tunnel(new_feature)
    #                 except IndexError:
    #                     pass
    #             initial_feature = new_feature
    #         if initial_feature.id == "h_tunnel" or initial_feature.id == "v_tunnel":
    #             center_x, center_y = initial_feature.center()
    #             if direction == "N":
    #                 w = random.randint(0, 10)
    #                 h = random.randint(0, 10)
    #                 new_feature = features.Room(center_x - w//2 - h, center_y,
    #                                    w, h)
    #                 try:
    #                     self.Room(new_feature)
    #                 except IndexError:
    #                     pass
    #             if direction == "E":
    #                 w = random.randint(0, 10)
    #                 h = random.randint(0, 10)
    #                 new_feature = features.Room(center_x - w//2 - h, center_y,
    #                                    w, h)
    #                 try:
    #                     self.Room(new_feature)
    #                 except IndexError:
    #                     pass
    #             if direction == "S":
    #                 w = random.randint(0, 10)
    #                 h = random.randint(0, 10)
    #                 new_feature = features.Room(center_x - w//2 - h, center_y,
    #                                    w, h)
    #                 try:
    #                     self.Room(new_feature)
    #                 except IndexError:
    #                     pass
    #             if direction == "W":
    #                 w = random.randint(0, 10)
    #                 h = random.randint(0, 10)
    #                 new_feature = features.Room(center_x - w//2 - h, center_y,
    #                                    w, h)
    #                 try:
    #                     self.Room(new_feature)
    #                 except IndexError:
    #                     pass
    #             rooms += 1

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
