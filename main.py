import tdl
import pdb
from game import constants

playerx = constants.SCREEN_WIDTH // 2
playery = constants.SCREEN_HEIGHT // 2


def handle_keys(entity):

    keypress = False
    for event in tdl.event.get():
        if event.type == 'KEYDOWN':
            user_input = event
            keypress = True
    if not keypress:
        return
    # movement keys
    if user_input.key == 'ESCAPE':
        return True
    if user_input.key == 'UP':
        entity.move(0, -1)

    elif user_input.key == 'DOWN':
        entity.move(0, 1)

    elif user_input.key == 'LEFT':
        entity.move(-1, 0)

    elif user_input.key == 'RIGHT':
        entity.move(1, 0)


def runGame(con):
    pass

def mainMenu(con):
	gui.draw_str(10, 9, 'T\'s Arena', bg=None, fg=(10, 117, 111))
        gui.draw_str(10, 10, 'Pick an option', bg=None, fg=(10, 117, 111))
        gui.draw_str(10, 12, '1> Start a new game', bg=None, fg=(10, 117, 111))
        gui.draw_str(10, 13, '2> Load game', bg=None, fg=(10, 117, 111))
        gui.draw_str(10, 14, '3> Join game', bg=None, fg=(10, 117, 111))
        root.blit(gui, 0, 0, constants.SCREEN_WIDTH,
                  constants.SCREEN_HEIGHT, 0, 0)
        tdl.flush()
    return True:

if __name__ == "__main__":
    tdl.set_font('terminal12x12.png', greyscale=True)
    root = tdl.init(constants.SCREEN_WIDTH,
                    constants.SCREEN_HEIGHT, title="TRL", fullscreen=False)
    gui = tdl.Console(constants.SCREEN_WIDTH, constants.SCREEN_WIDTH)
    con = tdl.Console(constants.SCREEN_WIDTH, constants.SCREEN_WIDTH)
    tdl.setFPS(constants.LIMIT_FPS)
    menu = True
    game = False
    while not tdl.event.is_window_closed():
        gui.draw_str(10, 9, 'T\'s Arena', bg=None, fg=(10, 117, 111))
        gui.draw_str(10, 10, 'Pick an option', bg=None, fg=(10, 117, 111))
        gui.draw_str(10, 12, '1> Start a new game', bg=None, fg=(10, 117, 111))
        gui.draw_str(10, 13, '2> Load game', bg=None, fg=(10, 117, 111))
        gui.draw_str(10, 14, '3> Join game', bg=None, fg=(10, 117, 111))
        root.blit(gui, 0, 0, constants.SCREEN_WIDTH,
                  constants.SCREEN_HEIGHT, 0, 0)
        tdl.flush()
