import pandas
from psychopy import visual, core, event
import helpers
import SetupDF

INSTRUCTION_PATH_PREFIX = "./img/instructions/"
SUFFIX = ".jpg"


def show_instructions(win: visual.Window, params, img: visual.ImageStim, Df: pandas.DataFrame):
    dict = SetupDF.create_dict_for_df(params, step="Instructions")
    for i in range(16):
        img.image = INSTRUCTION_PATH_PREFIX + "Slide" + str(i + 1) + SUFFIX
        img.setSize((2, 2))  # Size needs to be reset after changing the image
        img.draw()
        win.update()
        if i != 16:
            dict["Round"] = i
            Df = helpers.wait_for_space(win, Df, dict)
    key = event.getKeys()
    while 'r' not in key and 'space' not in key:
        dict["Round"] = 16
        Df = helpers.wait_for_space(win, Df, dict)
        key = event.getKeys()
    if 'r' in key:
        Df = show_instructions(win, params, img, Df)
    return Df
