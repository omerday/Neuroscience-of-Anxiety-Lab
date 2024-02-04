import pandas as pd
from psychopy import visual, core, event
import random
import helpers
import time
from psychopy.iohub.client.keyboard import Keyboard
from psychopy.visual import ratingscale
import dataHandler
import serialHandler

PATH = "./img/blocks/"
SUFFIX = ".jpg"

BLOCK_LENGTH = 120
CUE_LENGTH = 12
STARTLES_PER_BLOCK = 6

FIXED_CUE_TIMES = [30, 60, 90]

CONDITIONS = {"N": "Neutral", "P": "Predictable", "U": "Unpredictable"}

SCENARIO_PREFIX = {"N": 0, "P": 100, "U": 200}
STARTLE_EVENT_INDEX = 1
SHOCK_EVENT_INDEX = 2
CONDITION_START_INDEX = 10
CUE_START_INDEX = 20
CUE_END_INDEX = 30

SCALE_LABEL_HEB = "רמת חרדה"
SCALE_LABEL_ENG = "Anxiety Level"


def run_condition(window: visual.Window, image: visual.ImageStim, params: dict, io, condition: str, df: pd.DataFrame,
                  mini_df: pd.DataFrame, blockNum: int, ser=None, fear_level=5, sound=None):
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

    dict_for_df = dataHandler.create_dict_for_df(params=params, Step="Game", Block=blockNum, Scenario=CONDITIONS[condition])
    dict_for_df["ScenarioIndex"] = SCENARIO_PREFIX[condition] + CONDITION_START_INDEX
    dict_for_df["CurrentTime"] = round(time.time() - dict_for_df["StartTime"], 2)
    condition_start = time.time()
    dict_for_df["TimeInCondition"] = round(time.time() - condition_start, 2)
    mini_df = pd.concat([mini_df, pd.DataFrame.from_records([dict_for_df])])

    if params["recordPhysio"]:
        serialHandler.report_event(ser, dict_for_df["ScenarioIndex"])
    dict_for_df["ScenarioIndex"] = dict_for_df[
                                       "ScenarioIndex"] - CONDITION_START_INDEX  # Remove the condition-start event, and only
    # keep the condition we're in

    if condition == 'N':
        shock_time = 0
    else:
        shock_time, startle_times = helpers.randomize_shock(cue_times, startle_times,
                                                            True if condition == 'P' else False, params)
        shock_time = shock_time + time.time()

    cue_times, startle_times = helpers.prepare_cues_and_startles(cue_times, startle_times)

    timing_index = 0
    start_time = time.time()

    while time.time() < start_time + BLOCK_LENGTH:
        image.image = f"{PATH}{condition}_{params['language'][0]}{SUFFIX}"
        image.setSize((2, 2))
        image.draw()
        window.update()

        fear_level, df, mini_df = launch_wait_sequence(params=params, window=window, image=image,
                                                       end_time=cue_times[timing_index] if timing_index < 3
                                                       else start_time + BLOCK_LENGTH,
                                                       startles=startle_times, io=io, shock_time=shock_time,
                                                       fear_level=fear_level,
                                                       dict_for_df=dict_for_df, df=df, mini_df=mini_df, ser=ser,
                                                       condition_start=condition_start, sound=sound)

        if timing_index == 3:
            pass
        elif cue_times[timing_index] <= time.time() <= cue_times[timing_index] + 1:
            print("Entering a cue")
            current_cue_time = time.time()
            image.image = f"{PATH}{condition}_{params['language'][0]}_Cue{SUFFIX}"
            image.setSize((2, 2))
            # image.draw()
            # window.update()

            fear_level, df, mini_df = launch_wait_sequence(params=params, window=window, image=image,
                                                           end_time=current_cue_time + CUE_LENGTH,
                                                           startles=startle_times, io=io, shock_time=shock_time,
                                                           fear_level=fear_level,
                                                           cue=True, dict_for_df=dict_for_df, df=df, mini_df=mini_df,
                                                           ser=ser, condition_start=condition_start, sound=sound)
            timing_index += 1
            print("Leaving a cue")

    dataHandler.save_backup(params=params, fullDF=df, miniDF=mini_df)

    return fear_level, df, mini_df


def launch_wait_sequence(params: dict, window: visual.Window, image: visual.ImageStim, end_time, startles: list, io,
                         dict_for_df: dict, df: pd.DataFrame, mini_df: pd.DataFrame, shock_time=0, fear_level=5,
                         cue=False, ser=None, condition_start=0.0, sound=None):
    """
    The method prepares the command for launching the wait sequence from the "Helpers" module.
    It takes the cues times, shock times (if there are any) and the end time of the current waiting sequence and organizes
    them into a command.
    """
    if cue:
        dict_for_df["CueStart"] = round(time.time() - condition_start, 2)
        dict_for_df["ScenarioIndex"] += CUE_START_INDEX
    else:
        dict_for_df["ScenarioIndex"] += CUE_END_INDEX

    if params["recordPhysio"]:
        serialHandler.report_event(ser, dict_for_df["ScenarioIndex"])

    dict_for_df["Cue"] = 1 if cue else 0
    dict_for_df["CurrentTime"] = round(time.time() - dict_for_df["StartTime"], 2)
    dict_for_df["TimeInCondition"] = round(time.time() - condition_start, 2)
    mini_df = pd.concat([mini_df, pd.DataFrame.from_records([dict_for_df])])
    df = pd.concat([df, pd.DataFrame.from_records([dict_for_df])])

    startles_filtered = list(filter(lambda cue: time.time() <= cue <= end_time, startles))
    print(f"startles_filtered: {startles_filtered}")
    if shock_time != 0 and time.time() <= shock_time <= end_time:
        print("starting wait with shock")
        fear_level, df, mini_df = wait_in_condition(params=params, window=window, image=image,
                                                    startle_times=startles_filtered,
                                                    end_time=end_time, shock_time=shock_time, io=io,
                                                    fear_level=fear_level,
                                                    dict_for_df=dict_for_df, df=df, mini_df=mini_df, ser=ser,
                                                    condition_start=condition_start, sound=sound)
    else:
        print("starting wait without shock")
        fear_level, df, mini_df = wait_in_condition(window=window, image=image, startle_times=startles_filtered,
                                                    end_time=end_time, params=params, io=io, fear_level=fear_level,
                                                    dict_for_df=dict_for_df, df=df, mini_df=mini_df, ser=ser,
                                                    condition_start=condition_start, sound=sound)

    if cue:
        dict_for_df["CueEnd"] = round(time.time() - condition_start, 2)
        dict_for_df["CurrentTime"] = round(time.time() - dict_for_df["StartTime"], 2)
        dict_for_df["TimeInCondition"] = round(time.time() - condition_start, 2)
        mini_df = pd.concat([mini_df, pd.DataFrame.from_records([dict_for_df])])
        dict_for_df.pop("CueEnd")
        dict_for_df.pop("CueStart")
        dict_for_df["ScenarioIndex"] -= CUE_START_INDEX
    else:
        dict_for_df["ScenarioIndex"] -= CUE_END_INDEX

    return fear_level, df, mini_df


def wait_in_condition(window: visual.Window, image: visual.ImageStim, startle_times: list, end_time: time,
                      io, params: dict, dict_for_df: dict, df: pd.DataFrame, mini_df: pd.DataFrame, fear_level=5,
                      shock_time=0, ser=None, condition_start=0.0, sound=None):
    keyboard = io.devices.keyboard
    scale = ratingscale.RatingScale(win=window, scale=None, labels=["0", "10"], low=0, high=10, markerStart=fear_level,
                                    showAccept=False, markerColor="Gray", textColor="Black", lineColor="Black",
                                    pos=(0, -window.size[1] / 2 + 150))

    scale_label = visual.TextStim(win=window,
                                 text=SCALE_LABEL_ENG if params["language"] == "English" else SCALE_LABEL_HEB,
                                 pos=(0, -window.size[1] / 2 + 250), color="Black",
                                 languageStyle="LTR" if params["language"] == "English" else "RTL", height=40)

    while time.time() <= end_time:

        # Rating Scale
        image.draw()
        scale.draw()
        scale_label.draw()
        window.flip()

        # Write to DF
        dict_for_df["CurrentTime"] = round(time.time() - dict_for_df["StartTime"], 2)
        dict_for_df["FearRating"] = scale.getRating()
        df = pd.concat([df, pd.DataFrame.from_records([dict_for_df])])

        # Startles and shocks
        dict_for_df["TimeInCondition"] = round(time.time() - condition_start, 2)
        if len(startle_times) == 0:
            pass
        elif startle_times[0] <= time.time() <= startle_times[0] + 0.5:
            df, mini_df = helpers.play_startle(dict_for_df, df, mini_df, ser)
            startle_times.remove(startle_times[0])
        if shock_time <= time.time() <= shock_time + 0.3:
            df, mini_df = initiate_shock(params, dict_for_df, df, mini_df, ser, sound)

        # Escape
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == "escape":
                dataHandler.export_raw_data(params, df)
                dataHandler.export_summarized_dataframe(params, mini_df)
                window.close()
                core.quit()

    print(f"Scale Rating: {scale.getRating()}")
    return scale.getRating(), df, mini_df


def initiate_shock(params: dict, dict_for_df: dict, df: pd.DataFrame, mini_df: pd.DataFrame, ser=None, sound=None):
    dict_for_df["CurrentTime"] = round(time.time() - dict_for_df["StartTime"], 2)
    dict_for_df["Shock"] = 1
    dict_for_df["ScenarioIndex"] += SHOCK_EVENT_INDEX
    mini_df = pd.concat([mini_df, pd.DataFrame.from_records([dict_for_df])])

    if ser is not None:
        serialHandler.report_event(ser, dict_for_df["ScenarioIndex"])

    if params["shockType"] == "Shock":
        # TODO: Add shock mechanism
        pass
    else:
        df = helpers.play_shock_sound(dict_for_df, df, sound)

    dict_for_df.pop("Shock")
    dict_for_df["ScenarioIndex"] -= SHOCK_EVENT_INDEX
    return df, mini_df
