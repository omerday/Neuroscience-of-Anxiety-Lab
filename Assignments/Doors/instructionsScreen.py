import time
import datetime
import pandas
from psychopy import visual, core, event
import helpers
import dataHandler
import DoorPlay
import DoorPlayInfra

INSTRUCTION_PATH_HEBREW = "./img/InstructionsHebrew/"
INSTRUCTION_PATH_ENGLISH = "./img/InstructionsEnglish/"
SUFFIX = ".jpeg"
SLIDES = 25


def show_instructions(win: visual.Window, params, Df: pandas.DataFrame, miniDf: pandas.DataFrame,
                      summaryDf: pandas.DataFrame, io, ser=None):
    dict_for_df = dataHandler.create_dict_for_df(params, Section="Instructions")
    img = visual.ImageStim(win=win, units="norm", opacity=1,
                             size=(2, 2) if not params['fullScreen'] else None)
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

        dict_for_df["Round"] = i
        if i != 23:  # Check if replay slide is on
            if params["keyboardMode"]:
                Df = helpers.wait_for_space(win, Df, dict_for_df, io, params, miniDf)
            else:
                Df = helpers.wait_for_joystick_press(win, Df, dict_for_df, params, miniDf)
        else:
            # If replay slide is on, wait for a "replay" command and reset the index accordingly to start the
            # instructions from the beginning
            if params["keyboardMode"]:
                Df, again = helpers.wait_for_space_with_replay(win, Df, dict_for_df, io, params, miniDf)
            else:
                Df, again = helpers.wait_for_joystick_press_with_replay(win, Df, dict_for_df, params, miniDf)
            if again:
                i = 1
        dict_for_df['CurrentTime'] = round(time.time() - dict_for_df['StartTime'], 2)
        miniDf = pandas.concat([miniDf, pandas.DataFrame.from_records([dict_for_df])])

        if i == 14:  # Trigger a practice run
            Df, miniDf, summaryDf = DoorPlay.practice_run(
                                window=win, params=params, Df=Df, miniDf=miniDf, summary_df=summaryDf, io=io, ser=ser)

        if i == 22:  # Trigger a simulation run
            Df, mini_df, summaryDf, totalCoins = DoorPlay.run_task(
                                window=win, params=params, roundNum=0, totalCoins=0, Df=Df, miniDf=miniDf,
                                summary_df=summaryDf, io=io, ser=ser)

        if i == 24:   # Trigger a wheel run
            DoorPlayInfra.show_wheel(win, params, io)
    del img

    return Df, miniDf, summaryDf