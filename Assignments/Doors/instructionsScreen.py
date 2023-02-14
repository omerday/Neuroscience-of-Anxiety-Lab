from psychopy import visual, core, event
import helpers

INSTRUCTION_PATH_PREFIX = "./img/instructions/"
SUFFIX = ".jpg"


def show_instructions(win, params, img):
    for i in range(16):
        img.image = INSTRUCTION_PATH_PREFIX + "Slide" + str(i + 1) + SUFFIX
        img.setSize((params['screenSize'][0], params['screenSize'][1]))  # Size needs to be reset after changing the image
        img.draw()
        win.update()
        helpers.wait_for_space(win)
