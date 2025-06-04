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
import serialHandler

HABITUATION_STARTLES = 9
HABITUATION_EVENT = 80

SOUNDS = ["./sounds/shock_sound_1.mp3", "./sounds/shock_sound_2.mp3"]


def wait_for_space_no_df(window: visual.Window, io):
    keyboard = io.devices.keyboard
    keyboard.getKeys()
    core.wait(0.05)
    while True:
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == " ":
                return
            if event.key == "escape":
                window.close()
                core.quit()


def wait_for_space(window: visual.Window, io, params: dict, df: pd.DataFrame, dict_for_df: dict):
    keyboard = io.devices.keyboard
    keyboard.getKeys()
    core.wait(0.05)
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
        core.wait(0.05)


def wait_until_time_with_df(window: visual.Window, io, params: dict, df: pd.DataFrame, dict_for_df: dict, end_time):
    keyboard = io.devices.keyboard
    while time.time() < end_time:
        dict_for_df["CurrentTime"] = round(time.time() - params["startTime"], 2)
        df = pd.concat([df, pd.DataFrame.from_records([dict_for_df])])
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == "escape":
                dataHandler.export_raw_data(params, df)
                window.close()
                core.quit()
        core.wait(0.01)
    return df


def wait_for_space_with_replay(window: visual.Window, io, params: dict, df: pd.DataFrame, dict_for_df: dict):
    keyboard = io.devices.keyboard
    keyboard.getKeys()
    core.wait(0.05)
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


def wait_for_calibration(window: visual.Window, params, io, df: pd.DataFrame, mini_df: pd.DataFrame,
                         dict_for_df: dict, ser=None):
    keyboard = io.devices.keyboard
    start_time = time.time()
    dict_for_df["Step"] = "Calibration"
    dict_for_df["CurrentTime"] = round(time.time() - params["startTime"], 2)
    dict_for_df["ScenarioIndex"] = 99

    if params["recordPhysio"]:
        serialHandler.report_event(ser, dict_for_df["ScenarioIndex"])

    mini_df = pd.concat([mini_df, pd.DataFrame.from_records([dict_for_df])])
    dict_for_df.pop("ScenarioIndex")

    while time.time() < start_time + params["calibrationTime"]:
        dict_for_df["CurrentTime"] = round(time.time() - params["startTime"], 2)
        df = pd.concat([df, pd.DataFrame.from_records([dict_for_df])])
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == "escape":
                dataHandler.export_data(params=params, fullDF=df, miniDF=mini_df)
                window.close()
                core.quit()
        core.wait(0.05)

    return df, mini_df


def play_sound_and_wait(window: visual.Window, io, params: dict, df: pd.DataFrame,
                        dict_for_df: dict, sound_type: str):
    sound_path = ""
    if sound_type == "Scream":
        sound_path = "./sounds/shock_sound_1.mp3"
    elif sound_type == "Startle":
        sound_path = "./sounds/startle_probe.wav"
    soundToPlay = sound.Sound(sound_path)
    core.wait(3)
    now = ptb.GetSecs()
    soundToPlay.play(when=now)
    time_to_finish = time.time() + 2
    keyboard = io.devices.keyboard
    while time.time() < time_to_finish:
        dict_for_df["CurrentTime"] = round(time.time() - params["startTime"], 2)
        df = pd.concat([df, pd.DataFrame.from_records([dict_for_df])])
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == "escape":
                soundToPlay.stop()
                dataHandler.export_raw_data(params, df)
                window.close()
                core.quit()
        core.wait(0.05)
    while True:
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == "escape":
                dataHandler.export_raw_data(params, df)
                window.close()
                core.quit()
            elif event.key == " ":
                return
        core.wait(0.05)


def randomize_cue_times():
    random.seed()
    times = [random.randrange(8, 30), random.randrange(45, 70), random.randrange(85, 105)]
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
        for x in range(cue, cue + blocksInfra.CUE_LENGTH + 1):
            seconds.remove(x)
    for i in range(blocksInfra.STARTLES_PER_BLOCK - 3):
        chosen_sec = random.choice(seconds[int(i / 3 * len(seconds)): int((i + 1) / 3 * len(seconds))])
        startle_times.append(chosen_sec)
        seconds.remove(chosen_sec)
    startle_times.sort()

    print(f"startle times: {startle_times}")
    return startle_times


def randomize_shock(cues: list, startles: list, predictable: bool, params: dict):
    """
    The method randomizes a timing for the shock, given the restrictions.
    If we're in the Predicatble condition, we need to adjust the startle timing so there will be a 4-6 second diff between
    a startle and a shock (and the startle should come first)
    Args:
        cues:
        startles:
        predictable:
        params:

    Returns: shock_time, startles

    """
    random.seed()
    shock_time = 0
    resolve_cue_conflict = False
    if predictable:
        cue_for_shock = round(random.choice([0, 1, 2]), 2)
        if params["skipStartle"]:
            shock_time = round(cues[cue_for_shock] + random.uniform(2, 10), 2)
        else:
            shock_time = round(cues[cue_for_shock] + random.uniform(6, 8), 2)
            resolve_cue_conflict = True

    else:
        shock_time = round(random.randrange(10, blocksInfra.BLOCK_LENGTH - 10), 2)
        for cue in cues:
            if cue <= shock_time <= cue + blocksInfra.CUE_LENGTH:
                if params["skipStartle"]:
                    if not cue + 2 <= shock_time <= cue + blocksInfra.CUE_LENGTH - 2:
                        shock_time = round(random.randrange(cue + 2, cue + blocksInfra.CUE_LENGTH - 2), 2)
                else:
                    shock_time = round(cue + random.uniform(6, 8), 2)
                    resolve_cue_conflict = True

    if resolve_cue_conflict:
        cue_time = 0
        for cue in cues:
            if cue <= shock_time <= cue + blocksInfra.CUE_LENGTH:
                cue_time = cue
        new_startle = round(cue_time + random.uniform(1.5, 3.5), 2)
        for startle in startles:
            if cue_time < startle < cue_time + blocksInfra.CUE_LENGTH:
                startles.remove(startle)
                startles.append(new_startle)
                startles.sort()

    print(f"Shock is in {shock_time} seconds")
    print(f"Final startles are: {startles}")
    return shock_time, startles


def prepare_cues_and_startles(cues: list, startles: list):
    start_time = time.time()
    cue_times = []
    startle_times = []
    for cue in cues:
        cue_times.append(cue + start_time)
    for startle in startles:
        startle_times.append(startle + start_time)
    return cue_times, startle_times


def play_startle(dict_for_df: dict, df: pd.DataFrame, mini_df: pd.DataFrame, ser=None):
    dict_for_df["CurrentTime"] = round(time.time() - dict_for_df["StartTime"], 2)
    dict_for_df["Startle"] = 1
    dict_for_df["ScenarioIndex"] += blocksInfra.STARTLE_EVENT_INDEX

    mini_df = pd.concat([mini_df, pd.DataFrame.from_records([dict_for_df])])

    if ser is not None:
        serialHandler.report_event(ser, dict_for_df["ScenarioIndex"])

    soundToPlay = sound.Sound("./sounds/startle_probe_low.wav")
    now = ptb.GetSecs()
    now_for_while = time.time()
    soundToPlay.play(when=now)
    while time.time() < now_for_while + 1:
        dict_for_df["CurrentTime"] = round(time.time() - dict_for_df["StartTime"], 2)
        df = pd.concat([df, pd.DataFrame.from_records([dict_for_df])])
        core.wait(0.05)
    dict_for_df.pop("Startle")
    dict_for_df["ScenarioIndex"] -= blocksInfra.STARTLE_EVENT_INDEX
    return df, mini_df


def play_shock_sound(dict_for_df: dict, df: pd.DataFrame, sound_name=None):
    sound_path = sound_name if sound_name else "./sounds/shock_sound_1.mp3"
    soundToPlay = sound.Sound(sound_path)
    now = ptb.GetSecs()
    soundToPlay.play(when=now)
    now_for_while = time.time()

    while time.time() < now_for_while + 1.5:
        dict_for_df["CurrentTime"] = round(time.time() - dict_for_df["StartTime"], 2)
        df = pd.concat([df, pd.DataFrame.from_records([dict_for_df])])
        core.wait(0.05)
    return df


def play_shock_with_spider(window: visual.Window, dict_for_df: dict, df: pd.DataFrame, sound_name=None):
    image = visual.ImageStim(win=window, image="./img/spider.png",
                         units="norm", opacity=1,
                         size=(2, 2))
    image.draw()
    return play_shock_sound(dict_for_df, df, sound_name)


def startle_habituation_sequence(window: visual.Window, image: visual.ImageStim, params: dict, io, df: pd.DataFrame,
                                 mini_df: pd.DataFrame, ser=None):
    """
    The method sounds 8 startles in a randomized time, to create habituation effect and check the general physiological response.
    Each of the startles sends the BioPac a 80 event.
    Args:
        window: visual.Window component
        image: visual.ImageStim component
        params: parameters dictionary
        io: i/o object from the main code
        df:
        mini_df:
        ser: serial object for communication with the BioPac.

    Returns:

    """
    image.image = f"./img/habituation{params['language'][0]}.jpeg"
    image.setSize((2, 2))
    image.draw()
    window.update()
    window.mouseVisible = False

    dict_for_df = dataHandler.create_dict_for_df(params, Step="Habituation Sequence", ScenarioIndex=HABITUATION_EVENT)

    df = wait_until_time_with_df(window, io, params, df, dict_for_df, time.time() + 4)

    for i in range(1, HABITUATION_STARTLES + 1):
        wait_end_time = time.time() + random.uniform(5, 7)
        if params["recordPhysio"]:
            serialHandler.report_event(ser, HABITUATION_EVENT)
        dict_for_df["HabituationNum"] = i
        mini_df = pd.concat([mini_df, pd.DataFrame.from_records([dict_for_df])])

        soundToPlay = sound.Sound("./sounds/startle_probe_low.wav")
        now = ptb.GetSecs()
        soundToPlay.play(when=now)
        core.wait(0.5)

        df = wait_until_time_with_df(window, io, params, df, dict_for_df, wait_end_time)

    return df, mini_df


def randomize_sounds():
    """
    The method creates a permutation of two of the first sound and two of the second, to go along the block.
    """
    numbers = [0, 1, 2, 3]
    random.shuffle(numbers)
    sounds_in_order = []
    for x in numbers:
        sounds_in_order.append(SOUNDS[x % 2])
    print(sounds_in_order)
    return sounds_in_order

