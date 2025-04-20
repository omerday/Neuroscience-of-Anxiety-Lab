import time
from psychopy import visual, core
from psychopy.iohub.client.keyboard import Keyboard
import random
import VAS

NUM_OF_SLIDES = 23


def instructions(window: visual.Window, params, io):
    keyboard = io.devices.keyboard
    if params['language'] == 'English':
        name_prefix = "Instructions_E_"
    elif params['gender'] == 'Female':
        name_prefix = "Instructions_F_"
    else:
        name_prefix = "Instructions_M_"

    i = 2
    while i < NUM_OF_SLIDES + 1:
        if 3 <= i <= NUM_OF_SLIDES:
            image = visual.ImageStim(window, image=f"./img/instructions/{name_prefix}{i}_P2.jpeg", units="norm", size=(2, 2))
        else:
            image = visual.ImageStim(window, image=f"./img/instructions/{name_prefix}{i}.jpeg", units="norm", size=(2, 2))
        image.draw()
        window.flip()

        # Clearing events list
        keyboard.getKeys()
        core.wait(0.05)

        space = False
        while not space:
            core.wait(0.05)
            for event in keyboard.getKeys():
                if event.key == "escape":
                    window.close()
                    core.quit()
                elif event.key in [" ", 'c']:
                    i += 1
                    space = True
                elif i == NUM_OF_SLIDES and event.key == 'r':
                    instructions(window, params, io)
                    i += 1
                    space = True
                elif i > 2 and event.key == 'r':
                    i -= 1
                    space = True
