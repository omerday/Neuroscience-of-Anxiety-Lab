import pandas as pd
from psychopy import visual, core, event
from psychopy.iohub import launchHubServer
from psychopy.iohub.client.keyboard import Keyboard
from psychopy.visual import ratingscale
from psychopy import sound
import psychtoolbox as ptb
import time
import random

import blocksInfra
import dataHandler

CALIBRATION_TIME = 60


def wait_for_space_no_df(window: visual.Window, io):
    keyboard = io.devices.keyboard
    while True:
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == " ":
                return
            if event.key == "escape":
                window.close()
                core.quit()


def wait_for_space(window: visual.Window, io, params: dict, df: pd.DataFrame, dict_for_df: dict):
    keyboard = io.devices.keyboard
    while True:
        dict_for_df["CurrentTime"] = round(time.time() - params["startTime"], 2)
        df = pd.concat([df, pd.DataFrame.from_records([dict_for_df])])
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == " ":
                return df
            if event.key == "escape":
                dataHandler.export_raw_data(params, df)
                window.close()
                core.quit()


def wait_for_space_with_replay(window: visual.Window, io, params: dict, df: pd.DataFrame, dict_for_df: dict):
    keyboard = io.devices.keyboard
    while True:
        dict_for_df["CurrentTime"] = round(time.time() - params["startTime"], 2)
        df = pd.concat([df, pd.DataFrame.from_records([dict_for_df])])
        keys = keyboard.getPresses()
        for event in keys:
            if event.key == 'r' or event.key == 'R':
                return True, df
            elif event.key == ' ':
                return False, df
            elif event.key == "escape":
                dataHandler.export_raw_data(params, df)
                window.close()
                core.quit()


def wait_for_space_with_rating_scale(window, img: visual.ImageStim, io, params: dict, df: pd.DataFrame,
                                     dict_for_df: dict):
    keyboard = io.devices.keyboard
    print(-params["screenSize"][1] / 2 + 100)
    scale = ratingscale.RatingScale(win=window, scale=None, labels=["0", "10"], low=0, high=10, markerStart=5,
                                    showAccept=False, markerColor="Gray",
                                    acceptKeys=["space"], textColor="Black", lineColor="Black",
                                    pos=(0, -window.size[1] / 2 + 200))
    while scale.noResponse:
        dict_for_df["CurrentTime"] = round(time.time() - params["startTime"], 2)
        dict_for_df["FearRating"] = scale.getRating()
        df = pd.concat([df, pd.DataFrame.from_records([dict_for_df])])

        img.draw()
        scale.draw()
        window.flip()

    return df


def wait_for_calibration(window: visual.Window, params, io, df: pd.DataFrame, mini_df: pd.DataFrame, dict_for_df: dict):
    keyboard = io.devices.keyboard
    start_time = time.time()
    dict_for_df["Step"] = "Calibration"
    dict_for_df["CurrentTime"] = round(time.time() - params["startTime"], 2)

    if params["recordPhysio"]:
        # TODO: Send signal and add it to the dict
        pass

    mini_df = pd.concat([mini_df, pd.DataFrame.from_records([dict_for_df])])

    while time.time() < start_time + CALIBRATION_TIME:
        dict_for_df["CurrentTime"] = round(time.time() - params["startTime"], 2)
        df = pd.concat([df, pd.DataFrame.from_records([dict_for_df])])
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == "escape":
                dataHandler.export_raw_data(params, df)
                window.close()
                core.quit()
        core.wait(0.05)

    return df, mini_df


def play_startle_and_wait(window: visual.Window, io, params: dict, df: pd.DataFrame,
                                     dict_for_df: dict):
    soundToPlay = sound.Sound("./sounds/startle_probe.wav")
    core.wait(2)
    now = ptb.GetSecs()
    soundToPlay.play(when=now)
    core.wait(1)
    keyboard = io.devices.keyboard
    while True:
        dict_for_df["CurrentTime"] = round(time.time() - params["startTime"], 2)
        df = pd.concat([df, pd.DataFrame.from_records([dict_for_df])])
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == " ":
                soundToPlay.stop()
                return df
            if event.key == "escape":
                dataHandler.export_raw_data(params, df)
                window.close()
                core.quit()


def randomize_cue_times():
    random.seed()
    times = [random.randrange(10, 35), random.randrange(45, 75), random.randrange(85, 110)]
    times.sort()

    print(f"cue times - {times}")
    return times


def randomize_startles(cues: list):
    random.seed()
    seconds = list(range(2, 120))
    startle_times = []
    for cue in cues:
        # Randomize startle within cues (between 2 secs from the beginning and 2 secs from the end
        startle_times.append(round(random.uniform(cue + 2, cue + blocksInfra.CUE_LENGTH - 1), 2))
        # Remove all the seconds with a cue in them for future randchoice
        for x in range(cue, cue + 9):
            seconds.remove(x)
    for i in range(blocksInfra.STARTLES_PER_BLOCK - 3):
        chosen_sec = random.choice(seconds[int(i / 3 * len(seconds)): int((i + 1) / 3 * len(seconds))])
        startle_times.append(chosen_sec)
        seconds.remove(chosen_sec)
    startle_times.sort()

    print(f"startle times: {startle_times}")
    return startle_times


def randomize_shock(cues: list, startles: list, predictable: bool, params: dict):
    random.seed()
    shock_time = 0
    if predictable:
        num_of_cue = random.randrange(0, 3)
        shock_time = round(random.uniform(cues[num_of_cue], cues[num_of_cue] + blocksInfra.CUE_LENGTH), 2)
        if not params["skipStartle"]:
            startle_in_cue = 0
            for startle_time in startles:
                if cues[num_of_cue] <= startle_time <= cues[num_of_cue] + blocksInfra.CUE_LENGTH:
                    startle_in_cue = startle_time
            while startle_in_cue - 2.5 < shock_time < startle_in_cue + 2.5:
                shock_time = round(random.uniform(cues[num_of_cue], cues[num_of_cue] + blocksInfra.CUE_LENGTH), 2)
    else:
        if params["skipStartle"]:
            shock_time = random.randrange(10, blocksInfra.BLOCK_LENGTH - 10)
        else:
            startle_near_shock = True
            while startle_near_shock:
                startle_near_shock = False
                shock_time = random.randrange(10, blocksInfra.BLOCK_LENGTH - 10)
                for startle_time in startles:
                    if abs(shock_time - startle_time) > 3:
                        startle_near_shock = True
    print(f"Shock is in {shock_time - time.time()} seconds")
    return shock_time


def prepare_cues_and_startles(cues: list, startles: list):
    start_time = time.time()
    cue_times = []
    startle_times = []
    for cue in cues:
        cue_times.append(cue + start_time)
    for startle in startles:
        startle_times.append(startle + start_time)
    return cue_times, startle_times


def play_startle(dict_for_df: dict, df: pd.DataFrame, mini_df: pd.DataFrame):
    dict_for_df["CurrentTime"] = round(time.time() - dict_for_df["StartTime"], 2)
    dict_for_df["Startle"] = 1
    mini_df = pd.concat([mini_df, pd.DataFrame.from_records([dict_for_df])])

    soundToPlay = sound.Sound("./sounds/startle_probe.wav")
    now = ptb.GetSecs()
    now_for_while = time.time()
    soundToPlay.play(when=now)
    while time.time() < now_for_while + 1:
        dict_for_df["CurrentTime"] = round(time.time() - dict_for_df["StartTime"], 2)
        df = pd.concat([df, pd.DataFrame.from_records([dict_for_df])])
        core.wait(0.05)
    dict_for_df.pop("Startle")
    return df, mini_df


def play_shock_sound(dict_for_df: dict, df: pd.DataFrame):
    soundToPlay = sound.Sound("./sounds/shock_sound.mp3")
    now = ptb.GetSecs()
    soundToPlay.play(when=now)
    now_for_while = time.time()

    while time.time() < now_for_while + 1.5:
        dict_for_df["CurrentTime"] = round(time.time() - dict_for_df["StartTime"], 2)
        df = pd.concat([df, pd.DataFrame.from_records([dict_for_df])])
        core.wait(0.05)
    return df
