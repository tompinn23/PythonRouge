
class Map():
    # A game map
    def __init__(self, map_width, map_height, map_file=None):
        self.map_width = map_width
        self.map_height = map_height
        if map_file is None:
            game_map = [[Tile(True) for y in range(map_height)]
                        for x in range(map_width)]
        else:
            game_map = map_file
        self.game_map = game_map


class Tile():
    # a tile of the map and its properties
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        # all tiles start unexplored
        self.explored = False

        # by default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight
