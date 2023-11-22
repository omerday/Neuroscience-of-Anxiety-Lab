import time
import datetime
import pandas
from psychopy import visual, core, event
import helpers
import dataHandler

INSTRUCTION_PATH_HEBREW = "./img/InstructionsHebrew/"
INSTRUCTION_PATH_ENGLISH= "./img/InstructionsEnglish/"
SUFFIX = ".jpeg"


def show_instructions(win: visual.Window, params, img: visual.ImageStim, Df: pandas.DataFrame, miniDf: pandas.DataFrame, io):
    dict = dataHandler.create_dict_for_df(params, Section="Instructions")
    if params["language"] == "Hebrew":
        path = INSTRUCTION_PATH_HEBREW
        slides = 18
    else:
        path = INSTRUCTION_PATH_ENGLISH
        slides = 17
    for i in range(slides):
        img.image = path + "Slide" + str(i + 1) + SUFFIX
        img.setSize((2, 2))  # Size needs to be reset after changing the image
        img.draw()
        win.update()
        if i != slides:
            dict["Round"] = i + 1
            if params["keyboardMode"]:
                Df = helpers.wait_for_space(win, Df, dict, io)
            else:
                Df = helpers.wait_for_joystick_press(win, Df, dict)
            dict['CurrentTime'] = round(time.time() - dict['StartTime'], 2)
            miniDf = pandas.concat([miniDf, pandas.DataFrame.from_records([dict])])
    dict["Round"] = slides
    if params["keyboardMode"]:
        Df, again = helpers.wait_for_space_with_replay(win, Df, dict, io)
    else:
        Df, again = helpers.wait_for_joystick_press_with_replay(win, Df, dict)
    dict['CurrentTime'] = round(time.time() - dict['StartTime'], 2)
    miniDf = pandas.concat([miniDf, pandas.DataFrame.from_records([dict])])
    if again and params["keyboardMode"]:
        Df = show_instructions(win, params, img, Df, miniDf, io)
    elif again:
        Df = show_instructions(win, params, img, Df, miniDf, io)

    dict['CurrentTime'] = round(time.time() - dict['StartTime'], 2)
    miniDf = pandas.concat([miniDf, pandas.DataFrame.from_records([dict])])

    return Df, miniDf
