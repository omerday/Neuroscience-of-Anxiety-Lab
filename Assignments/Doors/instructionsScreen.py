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
SLIDES = 27


def show_instructions(win: visual.Window, params, full_df: pandas.DataFrame, mini_df: pandas.DataFrame,
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
        if i != 25:  # Check if replay slide is on
            if params["keyboardMode"]:
                full_df = helpers.wait_for_space(win, full_df, dict_for_df, io, params, mini_df)
            else:
                full_df = helpers.wait_for_joystick_press(win, full_df, dict_for_df, params, mini_df)
        else:
            # If replay slide is on, wait for a "replay" command and reset the index accordingly to start the
            # instructions from the beginning
            if params["keyboardMode"]:
                full_df, again = helpers.wait_for_space_with_replay(win, full_df, dict_for_df, io, params, mini_df)
            else:
                full_df, again = helpers.wait_for_joystick_press_with_replay(win, full_df, dict_for_df, params, mini_df)
            if again:
                i = 1
        dict_for_df['CurrentTime'] = round(time.time() - dict_for_df['StartTime'], 2)
        mini_df = pandas.concat([mini_df, pandas.DataFrame.from_records([dict_for_df])])

        if i in [14, 15]:  # Trigger a practice run
            full_df, mini_df, summaryDf = DoorPlay.practice_run(
                                window=win, params=params, full_df=full_df, mini_df=mini_df, summary_df=summaryDf, io=io, ser=ser)

        if i == 24:  # Trigger a simulation run
            full_df, mini_df, summaryDf, totalCoins = DoorPlay.run_task(
                                window=win, params=params, roundNum=0, totalCoins=0, full_df=full_df, mini_df=mini_df,
                                summary_df=summaryDf, io=io, ser=ser)

        if i == 26:   # Trigger a wheel run
            DoorPlayInfra.show_wheel(win, params, io)
    del img

    return full_df, mini_df, summaryDf