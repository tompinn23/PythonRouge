# imports
from bearlibterminal import terminal
from game import Player
from network import Server
from network import Client
import logging, time
# Setup Logging to file specifing date and time added to message
logging.basicConfig(filename='coursework.log',
                    format='%(asctime)s %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.INFO)
# Load the terminal window and set config options
terminal.open()
terminal.set("window: size=70x50; font: terminal12x12.png, size=12x12;")
terminal.refresh()
# Load a player entity for testing
player = Player(2, 2, False, 100, "player", "TomP")


def handle_keys(entity):
    """Function for handling input for an entity specified in the arguments"""
    # First we check for input availiablity so terminal.read() is none
    # blocking.
    if terminal.has_input():
        key = terminal.read()
        # We check for what the key is and then do a specific action based on
        # that key.
        if key == terminal.TK_LEFT:
            entity.move(-1, 0)
        elif key == terminal.TK_RIGHT:
            entity.move(1, 0)
        elif key == terminal.TK_UP:
            entity.move(0, -1)
        elif key == terminal.TK_DOWN:
            entity.move(0, 1)
        if key == terminal.TK_CLOSE:
            return True


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
    server = Server("localhost", 34562)
    time.sleep(5)
    server.closeServer()



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
#Cleanly close the terminal window.
terminal.close()
