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


while True:
    terminal.put(player.x, player.y, '@')
    terminal.refresh()
    terminal.put(player.x, player.y, ' ')
    exit = handle_keys(player)
    if exit:
        break


terminal.close()
