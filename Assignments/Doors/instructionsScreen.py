import time

import pandas
from psychopy import visual, core, event
import helpers
import SetupDF

INSTRUCTION_PATH_PREFIX = "./img/instructions/"
SUFFIX = ".jpg"


def show_instructions(win: visual.Window, params, img: visual.ImageStim, Df: pandas.DataFrame):
    dict = SetupDF.create_dict_for_df(params, StepName="Instructions")
    for i in range(16):
        img.image = INSTRUCTION_PATH_PREFIX + "Slide" + str(i + 1) + SUFFIX
        img.setSize((2, 2))  # Size needs to be reset after changing the image
        img.draw()
        win.update()
        if i != 16:
            dict["Round"] = i + 1
            Df = helpers.wait_for_space(win, Df, dict)
    key = event.getKeys()
    dict["Round"] = 16
    while 'r' not in key and 'space' not in key and 'escape' not in key:
        dict['CurrentTime'] = pandas.to_datetime(time.time())
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        core.wait(1 / 120)
        key = event.getKeys()
    if 'r' in key:
        Df = show_instructions(win, params, img, Df)
    if 'esc' in key:
        win.close()
        core.quit()
    return Df
