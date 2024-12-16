import time
from psychopy import visual, core
from psychopy.iohub.client.keyboard import Keyboard
import random
import VAS

NUM_OF_SLIDES = 28


def instructions(window: visual.Window, params, io):
    keyboard = io.devices.keyboard
    if params['language'] == 'English':
        name_prefix = "Instructions_E_"
    elif params['gender'] == 'Female':
        name_prefix = "Instructions_F_"
    else:
        name_prefix = "Instructions_M_"

    for i in range(2, NUM_OF_SLIDES + 1):
        if params["paradigm"] == 2 and 3 <= i <= 22:
            image = visual.ImageStim(window, image=f"./img/instructions/{name_prefix}{i}_P2.jpeg", units="norm", size=(2, 2))
        elif params["paradigm"] == 2 and 23 <= i <= 27:
            continue
        else:
            image = visual.ImageStim(window, image=f"./img/instructions/{name_prefix}{i}.jpeg", units="norm", size=(2, 2))
        image.draw()
        window.flip()

        # Clearing events list
        keyboard.getKeys()
        core.wait(0.1)

        space = False
        while not space:
            for event in keyboard.getKeys():
                if event.key == "escape":
                    window.close()
                    core.quit()
                elif event.key == " ":
                    space = True
                elif i == 28 and event.key == 'r':
                    instructions(window, params, io)
                    space = True
