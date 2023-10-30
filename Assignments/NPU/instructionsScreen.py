import time
import datetime
import pandas
from psychopy import visual, core, event
import helpers

PATH = "./img/instructions/"
SUFFIX = ".jpg"


def show_instructions(params: dict, win: visual.Window, img: visual.ImageStim, io):
    pref = f"{params['gender'][0]}{params['language'][0]}"
    for i in range(1, 22):
        img.image = f"{PATH}{i}{pref}{SUFFIX}"
        img.setSize((1,1))
        img.draw()
        win.update()
        helpers.wait_for_space(win, io)
