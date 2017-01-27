# imports
from bearlibterminal import terminal
from game.Player import Player
from game.Map import Map
from game import constants
from network.Client import Client
from network.Server import GameServer
import logging
import pickle
import time
import socket
from threading import Thread
from queue import Queue
import asyncio
# Setup Logging to file specifing date and time added to message
logging.basicConfig(filename='coursework.log',
                    format='%(asctime)s %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.INFO)
# Load the terminal window and set config options
terminal.open()
terminal.set("window: size=70x50; font: terminal12x12.png, size=12x12;")
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
    if key == terminal.TK_E:
        return "e"
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
        terminal.printf(4, 4, "2) Multiplayer")
        terminal.printf(4, 5, "3) Exit Game")
        terminal.refresh()
        # Then we wait for input.
        _exit = handle_input()
        # We return the value of the input choice.
        if _exit == 4533:
            return None
        elif _exit == 1:
            playGame()
        elif _exit == 2:
            multiMenu()
        elif _exit == 3:
            exit()


def playGame():
    _map = Map(70, 50)
    _map.generate_Dungeon(70, 50)
    playerx, playery = _map.findPlayerLoc()
    player = Player(playerx, playery, False, 100,'@', "player", "Tom")
    terminal.clear()
    _map.do_fov(player.x, player.y, constants.FOV_RADIUS)
    gameLoop(_map, player)

def gameLoop(_map, player):
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

def multiMenu():
    terminal.clear()
    terminal.printf(4, 2, "[color=(11,110,117)] Multiplayer")
    terminal.printf(4, 3, "1) Host Game")
    terminal.printf(4, 4, "2) Join Game")
    terminal.refresh()
    key = handle_input()
    if key == 1:
        hostGame()
    if key == 2:
        joinGame()
    if key == "e":
        mainMenu()

def hostGame():
    ip = socket.gethostbyname(socket.gethostname())
    s = GameServer(localaddr=(ip, 32078))
    terminal.clear()
    terminal.printf(4,3,"Your password is "+ip+":32078")
    terminal.printf(4,4, "Player list")
    terminal.refresh()
    
    


def joinGame():
    terminal.clear()
    terminal.printf(4, 3, "Enter Password:")
    conn = terminal.read_str(4,4, "", 22)
    addr = conn[1].split(":")
    terminal.clear()
    terminal.printf(4, 3, "Enter Nickname:")
    name = terminal.read_str(4,4, "", 10)
    client = Client(str(addr[0]), int(addr[1]), name)
    while client.isConnected == False:
        client.Loop()
        time.sleep(0.01)
        print("not connected")
    mpGameLoop(client, msgQ)

def mpGameLoop(client, msgQ):
    while True:
        client.Loop()
        if msgQ.qsize() > 0:
            msg = msgQ.get()
            print(msg)


if __name__ == "__main__":
    mainMenu()

    logging.info("----CLOSED PROGRAM----")
    # Cleanly close the terminal window.
    terminal.close()
