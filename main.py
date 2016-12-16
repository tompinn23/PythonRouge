from bearlibterminal import terminal
from game import Player
terminal.open()
terminal.set("window: size=70x50; font: terminal12x12.png, size=12x12;")
terminal.bkcolor
terminal.refresh()
player = Player(2, 2, False, 100, "player", "TomP")


def handle_keys(entity):
    if terminal.has_input():
        key = terminal.read()
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
    key = terminal.read()
    if key == terminal.TK_1:
        return 1
    if key == terminal.TK_2:
        return 2
    if key == terminal.TK_3:
        return 4533
    if key == terminal.TK_CLOSE:
        return 4533
    

def mainMenu():
    while True:
        terminal.printf(4, 2, "[color=(11,110,117)] Game")
        terminal.printf(4, 3, "1) Play Game")
        terminal.printf(4, 4, "2) Join Game")
        terminal.printf(4, 5, "3) Exit Game")
        exit = handle_input():
        if exit == 4533:
            break
            


terminal.close()
