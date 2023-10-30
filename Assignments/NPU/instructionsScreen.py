import time
import datetime
import pandas
from psychopy import visual, core, event
import helpers

PATH = "./img/instructions/"
SUFFIX = ".jpg"
SLIDES = 20


def show_instructions(params: dict, window: visual.Window, img: visual.ImageStim, io):
    pref = f"{params['gender'][0]}{params['language'][0]}"
    replay = True
    while replay:
        for i in range(1, SLIDES):
            img.image = f"{PATH}{i}{pref}{SUFFIX}"
            img.setSize((2,2))
            img.draw()
            window.update()
            if i == 4:
                # TODO: send calibration signal to the biopac
                # TODO: Change to 3 minutes in prod
                core.wait(5)
            elif i == 18:
                helpers.wait_for_space_with_rating_scale(window, img, io, params)
            elif i == 19:
                helpers.play_startle_and_wait(window, io)
            else:
                helpers.wait_for_space(window, io)
        # Last slide:
        img.image = f"{PATH}{SLIDES}{pref}{SUFFIX}"
        img.setSize((2,2))
        img.draw()
        window.update()
        replay = helpers.wait_for_space_with_replay(window, io)

        img.image = f"./img/start{params['language'][0]}{SUFFIX}"
        img.setSize((2,2))
        img.draw()
        window.update()
        helpers.wait_for_space(window, io)


def finalization(params: dict, window: visual.Window, img: visual.ImageStim, io):
    img.image = f"./img/finish{params['language'][0]}{SUFFIX}"
    img.setSize((2, 2))
    img.draw()
    window.update()
    helpers.wait_for_space(window, io)


def midpoint(params: dict, window: visual.Window, img: visual.ImageStim, io):
    img.image = f"./img/middle{params['gender'][0]}{params['language'][0]}{SUFFIX}"
    img.setSize((2, 2))
    img.draw()
    window.update()
    helpers.wait_for_space(window, io)

    img.image = f"./img/plus{SUFFIX}"
    img.setSize((2, 2))
    img.draw()
    window.update()
    # TODO: send calibration signal to the biopac
    # TODO: Change to 3 minutes in prod
    core.wait(5)

    img.image = f"./img/start{params['language'][0]}{SUFFIX}"
    img.setSize((2, 2))
    img.draw()
    window.update()
    helpers.wait_for_space(window, io)