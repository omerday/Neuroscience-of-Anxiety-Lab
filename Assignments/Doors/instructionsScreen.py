from psychopy import visual, core, event
import helpers

INSTRUCTION_PATH_PREFIX = "./img/instructions/"
SUFFIX = ".jpg"


def show_instructions(win, img, params):
    for i in range(16):
        img.image = INSTRUCTION_PATH_PREFIX + "Slide" + str(i + 1) + SUFFIX
        img.draw()
        win.update()
        helpers.wait_for_space(win)
