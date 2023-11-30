import random
import time
import datetime
import pandas
import pandas as pd
from psychopy import visual, core, event
import helpers
import dataHandler
from psychopy.iohub.client.keyboard import Keyboard


PATH = "./img/instructions/"
SUFFIX = ".jpeg"
SLIDES = 21
SHOCK_SLIDE = 7
STARTLE_SLIDE = 20
RATING_SLIDE = 19


def show_instructions(params: dict, window: visual.Window, img: visual.ImageStim, io, df: pd.DataFrame,
                      mini_df: pd.DataFrame, ser=None):
    pref = f"{params['gender'][0]}{params['language'][0]}"
    dict_for_df = dataHandler.create_dict_for_df(params, Step="Instructions")

    replay = True
    plays_again = False
    while replay:
        for i in range(1, SLIDES):
            if params["skipCalibration"] and i in [3, 4, 5]:
                pass
            elif params["skipStartle"] and i == STARTLE_SLIDE:
                pass
            elif not plays_again or (plays_again and i not in [3, 4, 5]):
                dict_for_df["InstructionScreenNum"] = i
                dict_for_df["CurrentTime"] = round(time.time() - params["startTime"], 2)
                mini_df = pd.concat([mini_df, pd.DataFrame.from_records([dict_for_df])])

                img.image = f"{PATH}{i}{pref}{SUFFIX}"
                img.setSize((2,2))
                img.draw()
                window.update()
                if i == 4:
                    df, mini_df = helpers.wait_for_calibration(window, params, io, df, mini_df, dict_for_df, ser)
                    dict_for_df["Step"] = "Instructions"
                elif i == SHOCK_SLIDE:
                    df = helpers.play_shock_and_wait(window, io, params, df, dict_for_df)
                elif i == RATING_SLIDE:
                    df = helpers.wait_for_space_with_rating_scale(window, img, io, params, df, dict_for_df)
                elif i == STARTLE_SLIDE:
                    df = helpers.play_startle_and_wait(window, io, params, df, dict_for_df)
                else:
                    df = helpers.wait_for_space(window, io, params, df, dict_for_df)

        # Last slide:
        img.image = f"{PATH}{SLIDES}{pref}{SUFFIX}"
        img.setSize((2,2))
        img.draw()
        window.update()
        replay, df = helpers.wait_for_space_with_replay(window, io, params, df, dict_for_df)
        plays_again = replay

    return df, mini_df


def finalization(params: dict, window: visual.Window, img: visual.ImageStim, io, df: pd.DataFrame, mini_df: pd.DataFrame):
    dict_for_df = dataHandler.create_dict_for_df(params, Step="Instructions")
    dict_for_df["InstructionScreenNum"] = "Final"
    dict_for_df["CurrentTime"] = round(time.time() - params["startTime"], 2)

    mini_df = pd.concat([mini_df, pd.DataFrame.from_records([dict_for_df])])

    img.image = f"./img/finish{params['language'][0]}{SUFFIX}"
    img.setSize((2, 2))
    img.draw()
    window.update()
    df = helpers.wait_for_space(window, io, params, df, dict_for_df)

    return df, mini_df


def midpoint(params: dict, window: visual.Window, img: visual.ImageStim, io, df: pd.DataFrame,
             mini_df: pd.DataFrame, ser=None):
    dict_for_df = dataHandler.create_dict_for_df(params, Step="Instructions")
    dict_for_df["InstructionScreenNum"] = "Middle"
    dict_for_df["CurrentTime"] = round(time.time() - params["startTime"], 2)

    mini_df = pd.concat([mini_df, pd.DataFrame.from_records([dict_for_df])])

    img.image = f"./img/middle{params['gender'][0]}{params['language'][0]}{SUFFIX}"
    img.setSize((2, 2))
    img.draw()
    window.update()
    df = helpers.wait_for_space(window, io, params, df, dict_for_df)

    img.image = f"./img/plus{SUFFIX}"
    img.setSize((2, 2))
    img.draw()
    window.update()

    df, mini_df = helpers.wait_for_calibration(window, params, io, df, mini_df, dict_for_df, ser)

    return df, mini_df


def start_screen(window: visual.Window, image: visual.ImageStim, params: dict, df: pandas.DataFrame, io):
    dict_for_df = dataHandler.create_dict_for_df(params, Step="Instructions", InstructionScreenNum="Start",)
    image.image = f"./img/start{params['language'][0]}{SUFFIX}"
    image.setSize((2, 2))
    image.draw()
    window.update()
    df = helpers.wait_for_space(window, io, params, df, dict_for_df)
    return df


def blank_screen(window: visual.Window, image: visual.ImageStim, params: dict, df: pandas.DataFrame, io, block: int,
                 condition: str):
    keyboard = io.devices.keyboard
    dict_for_df = dataHandler.create_dict_for_df(params, Step="Game", Block=block, Scenario=condition)
    image.image = f"./image/blank.jpeg"
    image.setSize((2, 2))
    image.draw()
    window.update()
    wait_end_time = time.time() + random.uniform(2, 4)
    while time.time() < wait_end_time:
        dict_for_df["CurrentTime"] = round(time.time() - params["startTime"], 2)
        df = pd.concat([df, pandas.DataFrame.from_records([dict_for_df])])
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == "escape":
                window.close()
                core.quit()
        core.wait(0.01)
    return df
