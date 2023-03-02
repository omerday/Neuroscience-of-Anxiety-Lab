from psychopy import visual, core, event
import helpers

INSTRUCTION_PATH_PREFIX = "./img/instructions/"
SUFFIX = ".jpg"


def show_instructions(win: visual.Window, params, img: visual.ImageStim):
    for i in range(16):
        img.image = INSTRUCTION_PATH_PREFIX + "Slide" + str(i + 1) + SUFFIX
        img.setSize((2, 2))  # Size needs to be reset after changing the image
        img.draw()
        win.update()
        if i != 16:
            helpers.wait_for_space(win)
    key = event.getKeys()
    while 'r' not in key and 'space' not in key:
        key = event.getKeys()
    if 'r' in key:
        show_instructions(win, params, img)
    return
