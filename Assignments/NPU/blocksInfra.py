import pandas as pd
from psychopy import visual, core, event
import random
import helpers
import time
from psychopy.iohub.client.keyboard import Keyboard
from psychopy.visual import ratingscale
import dataHandler


PATH = "./img/blocks/"
SUFFIX = ".jpg"

BLOCK_LENGTH = 120
CUE_LENGTH = 8
STARTLES_PER_BLOCK = 6

FIXED_CUE_TIMES = [30, 60, 90]


def run_condition(window: visual.Window, image: visual.ImageStim, params: dict, io, condition: str, df: pd.DataFrame,
                  mini_df: pd.DataFrame, blockNum: int):
    if condition != "N" and condition != "P" and condition != "U":
        print("Unknown condition " + condition)
        return

    print("Starting condition " + condition)
    print("Randomizing times")

    cue_times = helpers.randomize_cue_times()
    if not params["skipStartle"]:
        startle_times = helpers.randomize_startles(cue_times)
    else:
        startle_times = []

    cue_times, startle_times = helpers.prepare_cues_and_startles(cue_times, startle_times)

    dict_for_df = dataHandler.create_dict_for_df(params=params, Step="Game", Block=blockNum, Scenario=condition)

    if condition == 'N':
        shock_time = 0
    else:
        shock_time = helpers.randomize_shock(cue_times, startle_times, True if condition == 'P' else False, params)

    timing_index = 0
    start_time = time.time()
    fear_level = 5

    while time.time() < start_time + BLOCK_LENGTH:
        image.image = f"{PATH}{condition}_{params['language'][0]}{SUFFIX}"
        image.setSize((2, 2))
        image.draw()
        window.update()

        fear_level, df, mini_df = launch_wait_sequence(params=params, window=window, image=image,
                             end_time=cue_times[timing_index] if timing_index < 3 else start_time + BLOCK_LENGTH,
                             startles=startle_times, io=io, shock_time=shock_time, fear_level=fear_level,
                                          dict_for_df=dict_for_df, df=df, mini_df=mini_df)

        if timing_index == 3:
            pass
        elif cue_times[timing_index] <= time.time() <= cue_times[timing_index] + 1:
            print("Entering a cue")
            current_cue_time = time.time()
            image.image = f"{PATH}{condition}_{params['language'][0]}_Cue{SUFFIX}"
            image.setSize((2, 2))
            image.draw()
            window.update()

            fear_level, df, mini_df = launch_wait_sequence(params=params, window=window, image=image, end_time=current_cue_time + CUE_LENGTH,
                                 startles=startle_times, io=io, shock_time=shock_time, fear_level=fear_level,
                                              cue=True, dict_for_df=dict_for_df, df=df, mini_df=mini_df)
            timing_index += 1
            print("Leaving a cue")

    return df, mini_df


def wait_in_condition(window: visual.Window, image: visual.ImageStim, startle_times: list, end_time: time,
                     io, params: dict, dict_for_df: dict, df:pd.DataFrame, mini_df:pd.DataFrame, fear_level=5, shock_time=0):
    keyboard = io.devices.keyboard
    scale = ratingscale.RatingScale(win=window, scale=None, labels=["0", "10"], low=0, high=10, markerStart=fear_level,
                                    showAccept=False, markerColor="Red", textColor="Black", lineColor="Black",
                                    pos=(0, -window.size[1] / 2 + 200))

    while time.time() <= end_time:

        # Rating Scale
        image.draw()
        scale.draw()
        window.flip()

        # Write to DF
        dict_for_df["CurrentTime"] = round(time.time() - dict_for_df["StartTime"], 2)
        dict_for_df["FearRating"] = scale.getRating()
        df = pd.concat([df, pd.DataFrame.from_records([dict_for_df])])

        # Startles and shocks
        if len(startle_times) == 0:
            pass
        elif startle_times[0] <= time.time() <= startle_times[0] + 0.5:
            df, mini_df = helpers.play_startle(dict_for_df, df, mini_df)
            startle_times.remove(startle_times[0])
        if shock_time <= time.time() <= shock_time + 0.3:
            df, mini_df = initiate_shock(params, dict_for_df, df, mini_df)

        # Escape
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == "escape":
                dataHandler.export_raw_data(params, df)
                dataHandler.export_summarized_dataframe(params, mini_df)
                window.close()
                core.quit()

    print(f"Scale Rating: {scale.getRating()}")
    return scale.getRating(), df, mini_df


def launch_wait_sequence(params: dict, window: visual.Window, image: visual.ImageStim, end_time, startles: list, io,
                         dict_for_df: dict, df:pd.DataFrame, mini_df:pd.DataFrame, shock_time=0, fear_level=5, cue=False):
    """
    The method prepares the command for launching the wait sequence from the "Helpers" module.
    It takes the cues times, shock times (if there are any) and the end time of the current waiting sequence and organizes
    them into a command.
    """
    if cue:
        dict_for_df["CueStart"] = round(time.time() - dict_for_df["StartTime"], 2)
    dict_for_df["Cue"] = 1 if cue else 0
    dict_for_df["CurrentTime"] = round(time.time() - dict_for_df["StartTime"], 2)
    mini_df = pd.concat([mini_df, pd.DataFrame.from_records([dict_for_df])])
    df = pd.concat([df, pd.DataFrame.from_records([dict_for_df])])

    startles_filtered = list(filter(lambda cue: time.time() <= cue <= end_time, startles))
    print(f"startles_filtered: {startles_filtered}")
    if shock_time != 0 and time.time() <= shock_time <= end_time:
        print("starting wait with shock")
        fear_level, df, mini_df = wait_in_condition(params=params, window=window, image=image, startle_times=startles_filtered,
                                      end_time=end_time, shock_time=shock_time, io=io, fear_level=fear_level,
                                      dict_for_df=dict_for_df, df=df, mini_df=mini_df)
    else:
        print("starting wait without shock")
        fear_level, df, mini_df = wait_in_condition(window=window,  image=image, startle_times=startles_filtered,
                                         end_time=end_time, params=params, io=io, fear_level=fear_level,
                                         dict_for_df=dict_for_df, df=df, mini_df=mini_df)

    if cue:
        dict_for_df["CueEnd"] = round(time.time() - dict_for_df["StartTime"], 2)
        dict_for_df["CurrentTime"] = round(time.time() - dict_for_df["StartTime"], 2)
        mini_df = pd.concat([mini_df, pd.DataFrame.from_records([dict_for_df])])
        dict_for_df.pop("CueEnd")
        dict_for_df.pop("CueStart")

    return fear_level, df, mini_df


def initiate_shock(params: dict, dict_for_df: dict, df: pd.DataFrame, mini_df: pd.DataFrame):
    dict_for_df["CurrentTime"] = round(time.time() - dict_for_df["StartTime"], 2)
    dict_for_df["Shock"] = 1
    mini_df = pd.concat([mini_df, pd.DataFrame.from_records([dict_for_df])])

    if params["shockType"] == "Shock":
        # TODO: Add shock mechanism
        pass
    else:
        df = helpers.play_shock_sound(dict_for_df, df)

    dict_for_df.pop("Shock")
    return df, mini_df
