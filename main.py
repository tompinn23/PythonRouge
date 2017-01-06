# imports
from bearlibterminal import terminal
from game import Player
from game import Map
from game import Rect
from game import constants
from network import Server
from network import Client
import logging
import time
# Setup Logging to file specifing date and time added to message
logging.basicConfig(filename='coursework.log',
                    format='%(asctime)s %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.INFO)
# Load the terminal window and set config options
terminal.open()
terminal.set("window: size=70x50; font: terminal12x12.png, size=12x12;")
terminal_set("0x40: at.png, align=center");
terminal.refresh()
# Load a player entity for testing


def handle_keys(entity, _map):
    """Function for handling input for an entity specified in the arguments"""
    # First we check for input availiablity so terminal.read() is none
    # blocking.
    if terminal.has_input():
        key = terminal.read()
        # We check for what the key is and then do a specific action based on
        # that key.
        if key == terminal.TK_LEFT:
            entity.move(-1, 0, _map)
            return 1
        elif key == terminal.TK_RIGHT:
            entity.move(1, 0, _map)
            return 1
        elif key == terminal.TK_UP:
            entity.move(0, -1, _map)
            return 1
        elif key == terminal.TK_DOWN:
            entity.move(0, 1, _map)
            return 1
        if key == terminal.TK_CLOSE:
            return 2


def handle_input():
    """Function that handles more typical input such as choices etc."""
    # This is blocking as we need to wait for a key to be pressed.
    key = terminal.read()
    if key == terminal.TK_1:
        return 1
    if key == terminal.TK_2:
        return 2
    # This is randomly chosen close code allowing the program to exit when the
    # windows is closed or the exit option is chosen.
    if key == terminal.TK_3:
        return 4533
    if key == terminal.TK_CLOSE:
        return 4533


def mainMenu():
    """Function that loads the Main Menu"""
    while True:
        # First we clear the terminal then we print the options.
        terminal.clear()
        terminal.printf(4, 2, "[color=(11,110,117)] Game")
        terminal.printf(4, 3, "1) Play Game")
        terminal.printf(4, 4, "2) Join Game")
        terminal.printf(4, 5, "3) Exit Game")
        terminal.refresh()
        # Then we wait for input.
        _exit = handle_input()
        # We return the value of the input choice.
        if _exit == 4533:
            return None
        elif _exit == 1:
            return 1
        elif _exit == 2:
            return 2
        elif _exit == 3:
            return 3


def playGame():
    _map = Map(50, 50)
    _map.generate_Dungeon(50, 50)
    playerx, playery = _map.findPlayerLoc()
    player = Player(playerx, playery, False, 100,'@', "player", "Tom")
    terminal.clear()
    _map.do_fov(player.x, player.y, constants.FOV_RADIUS)
    while True:
        _map.render_map()
        _map.draw_player_background(player.x, player.y)
        terminal.layer(1)
        player.draw()
        terminal.refresh()
        player.clear()
        ex = handle_keys(player, _map.game_map)
        if ex == 1:
            _map.do_fov(player.x, player.y, constants.FOV_RADIUS)
        if ex == 2:
            break


def joinGame():
    pass


logging.info("Activated Main Menu")
# We get choice from the Main Menu then we either exit the game or do a
# specific function.
ch = mainMenu()
if ch == 1:
    playGame()
if ch == 2:
    joinGame()
if ch == 3:
    pass

logging.info("----CLOSED PROGRAM----")
# Cleanly close the terminal window.
terminal.close()
