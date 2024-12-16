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


def show_instructions(win: visual.Window, params, miniDf: pandas.DataFrame,
                      summaryDf: pandas.DataFrame, io, ser=None):
    """
    The method presents the set of instructions in the appropriate language, and launches any extra sequences needed.
    For example it runs example runs to show how to navigate, as well as simulation run of a few doors.
    All is based o the number of slide we're on, which can be found in ./img/instructionsHebrew
    Args:
        win: visual.Window object
        params: parameters dictionary
        Df:
        miniDf:
        summaryDf:
        io: i/o component from the main code
        ser: serial object for communication with the BioPac

    Returns: Given Dataframes

    """
    dict_for_df = dataHandler.create_dict_for_df(params, Section="Instructions")
    img = visual.ImageStim(win=win, units="norm", opacity=1,
                             size=(2, 2) if not params['fullScreen'] else None)
    if params["language"] == "Hebrew":
        path = INSTRUCTION_PATH_HEBREW
    else:
        path = INSTRUCTION_PATH_ENGLISH

    for i in range(1, SLIDES + 1):
        # Present the relevant instruction slide
        image_name = str(i) + ("H" if params["language"] == "Hebrew" else "E")
        img.image = path + image_name + SUFFIX
        img.setSize((2, 2))  # Size needs to be reset after changing the image
        img.draw()
        win.mouseVisible = False
        win.update()

        dict_for_df["Round"] = i
        if i != 25:  # Check if replay slide is on
            if params["keyboardMode"]:
                helpers.wait_for_space(win, io, params, miniDf)
            else:
                helpers.wait_for_joystick_press(win, params, miniDf)
        else:
            # If replay slide is on, wait for a "replay" command and reset the index accordingly to start the
            # instructions from the beginning
            if params["keyboardMode"]:
                again = helpers.wait_for_space_with_replay(win, io, params, miniDf)
            else:
                again = helpers.wait_for_joystick_press_with_replay(win, params, miniDf)
            if again:
                i = 1
        dict_for_df['CurrentTime'] = round(time.time() - dict_for_df['StartTime'], 2)
        miniDf = pandas.concat([miniDf, pandas.DataFrame.from_records([dict_for_df])])

        if i in [14, 15]:  # Trigger a practice run
            miniDf, summaryDf = DoorPlay.practice_run(
                                window=win, params=params, miniDf=miniDf, summary_df=summaryDf, io=io, ser=ser)

        if i == 24:  # Trigger a simulation run
            mini_df, summaryDf, totalCoins = DoorPlay.run_task(
                                window=win, params=params, blockNumber=0, totalCoins=0, miniDf=miniDf,
                                summary_df=summaryDf, io=io, ser=ser)

        if i == 26:   # Trigger a wheel run
            DoorPlayInfra.show_wheel(win, params, io)
    del img

    return miniDf, summaryDf