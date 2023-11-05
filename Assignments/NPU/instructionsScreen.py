import time
import datetime
import pandas
import pandas as pd
from psychopy import visual, core, event
import helpers
import dataHandler

PATH = "./img/instructions/"
SUFFIX = ".jpg"
SLIDES = 20


def show_instructions(params: dict, window: visual.Window, img: visual.ImageStim, io, df: pd.DataFrame,
                      mini_df: pd.DataFrame):
    pref = f"{params['gender'][0]}{params['language'][0]}"
    dict_for_df = dataHandler.create_dict_for_df(params, Step="Instructions")

    replay = True
    while replay:
        for i in range(1, SLIDES):
            dict_for_df["InstructionScreenNum"] = i
            dict_for_df["CurrentTime"] = round(time.time() - params["startTime"], 2)
            mini_df = pd.concat([mini_df, dict_for_df])

            img.image = f"{PATH}{i}{pref}{SUFFIX}"
            img.setSize((2,2))
            img.draw()
            window.update()
            if i == 4:
                df, mini_df = helpers.wait_for_calibration(window, params, io, df, mini_df, dict_for_df)
            elif i == 18:
                df = helpers.wait_for_space_with_rating_scale(window, img, io, params, df, dict_for_df)
            elif i == 19:
                df = helpers.play_startle_and_wait(window, io, params, df, dict_for_df)
            else:
                df = helpers.wait_for_space(window, io, params, df, dict_for_df)

        # Last slide:
        img.image = f"{PATH}{SLIDES}{pref}{SUFFIX}"
        img.setSize((2,2))
        img.draw()
        window.update()
        replay, df = helpers.wait_for_space_with_replay(window, io, params, df, dict_for_df)

        img.image = f"./img/start{params['language'][0]}{SUFFIX}"
        img.setSize((2,2))
        img.draw()
        window.update()

        dict_for_df["InstructionScreenNum"] = "Start"
        dict_for_df["CurrentTime"] = round(time.time() - params["startTime"], 2)
        mini_df = pd.concat([mini_df, dict_for_df])

        df = helpers.wait_for_space(window, io, params, df, dict_for_df)
        return df, mini_df


def finalization(params: dict, window: visual.Window, img: visual.ImageStim, io, df: pd.DataFrame, mini_df: pd.DataFrame):
    dict_for_df = dataHandler.create_dict_for_df(params, Step="Instructions")
    dict_for_df["InstructionScreenNum"] = "Final"
    dict_for_df["CurrentTime"] = round(time.time() - params["startTime"], 2)

    mini_df = pd.concat([mini_df, dict_for_df])

    img.image = f"./img/finish{params['language'][0]}{SUFFIX}"
    img.setSize((2, 2))
    img.draw()
    window.update()
    df = helpers.wait_for_space(window, io, params, df, dict_for_df)

    return df, mini_df


def midpoint(params: dict, window: visual.Window, img: visual.ImageStim, io, df: pd.DataFrame, mini_df: pd.DataFrame):
    dict_for_df = dataHandler.create_dict_for_df(params, Step="Instructions")
    dict_for_df["InstructionScreenNum"] = "Middle"
    dict_for_df["CurrentTime"] = round(time.time() - params["startTime"], 2)

    mini_df = pd.concat([mini_df, dict_for_df])

    img.image = f"./img/middle{params['gender'][0]}{params['language'][0]}{SUFFIX}"
    img.setSize((2, 2))
    img.draw()
    window.update()
    df = helpers.wait_for_space(window, io, params, df, dict_for_df)

    img.image = f"./img/plus{SUFFIX}"
    img.setSize((2, 2))
    img.draw()
    window.update()

    df, mini_df = helpers.wait_for_calibration(window, params, io, df, mini_df, dict_for_df)

    img.image = f"./img/start{params['language'][0]}{SUFFIX}"
    img.setSize((2, 2))
    img.draw()
    window.update()
    df = helpers.wait_for_space(window, io, params, df, dict_for_df)

    return df, mini_df
