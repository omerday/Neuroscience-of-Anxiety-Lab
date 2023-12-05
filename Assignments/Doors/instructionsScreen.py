import time
import datetime
import pandas
from psychopy import visual, core, event
import helpers
import dataHandler

INSTRUCTION_PATH_HEBREW = "./img/InstructionsHebrew/"
INSTRUCTION_PATH_ENGLISH= "./img/InstructionsEnglish/"
SUFFIX = ".jpg"
SLIDES = 19

def show_instructions(win: visual.Window, params, img: visual.ImageStim, Df: pandas.DataFrame, miniDf: pandas.DataFrame, io):
    dict_for_df = dataHandler.create_dict_for_df(params, Section="Instructions")
    if params["language"] == "Hebrew":
        path = INSTRUCTION_PATH_HEBREW
    else:
        path = INSTRUCTION_PATH_ENGLISH
    for i in range(1, SLIDES + 1):
        image_name = str(i) + ("H" if params["language"] == "Hebrew" else "E")
        img.image = path + image_name + SUFFIX
        img.setSize((2, 2))  # Size needs to be reset after changing the image
        img.draw()
        win.update()
        if i != SLIDES:
            dict_for_df["Round"] = i
            if params["keyboardMode"]:
                Df = helpers.wait_for_space(win, Df, dict_for_df, io, params, miniDf)
            else:
                Df = helpers.wait_for_joystick_press(win, Df, dict_for_df, params, miniDf)
            dict_for_df['CurrentTime'] = round(time.time() - dict_for_df['StartTime'], 2)
            miniDf = pandas.concat([miniDf, pandas.DataFrame.from_records([dict_for_df])])
    dict_for_df["Round"] = SLIDES
    if params["keyboardMode"]:
        Df, again = helpers.wait_for_space_with_replay(win, Df, dict_for_df, io, params, miniDf)
    else:
        Df, again = helpers.wait_for_joystick_press_with_replay(win, Df, dict_for_df, params, miniDf)
    dict_for_df['CurrentTime'] = round(time.time() - dict_for_df['StartTime'], 2)
    miniDf = pandas.concat([miniDf, pandas.DataFrame.from_records([dict_for_df])])
    if again and params["keyboardMode"]:
        Df = show_instructions(win, params, img, Df, miniDf, io)
    elif again:
        Df = show_instructions(win, params, img, Df, miniDf, io)

    dict_for_df['CurrentTime'] = round(time.time() - dict_for_df['StartTime'], 2)
    miniDf = pandas.concat([miniDf, pandas.DataFrame.from_records([dict_for_df])])

    return Df, miniDf
