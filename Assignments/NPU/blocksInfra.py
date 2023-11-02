from psychopy import visual, core, event
import random
import helpers
import time
from psychopy.iohub.client.keyboard import Keyboard
from psychopy.visual import ratingscale


PATH = "./img/blocks/"
SUFFIX = ".jpg"

BLOCK_LENGTH = 120
CUE_LENGTH = 8
STARTLES_PER_BLOCK = 6

FIXED_CUE_TIMES = [30, 60, 90]


def run_condition(window: visual.Window, image: visual.ImageStim, params: dict, io, condition: str):
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

        fear_level = launch_wait_sequence(params=params, window=window, image=image,
                             end_time=cue_times[timing_index] if timing_index < 3 else start_time + BLOCK_LENGTH,
                             startles=startle_times, io=io, shock_time=shock_time, fear_level=fear_level)

        if timing_index == 3:
            pass
        elif cue_times[timing_index] <= time.time() <= cue_times[timing_index] + 1:
            print("Entering a cue")
            current_cue_time = time.time()
            image.image = f"{PATH}{condition}_{params['language'][0]}_Cue{SUFFIX}"
            image.setSize((2, 2))
            image.draw()
            window.update()

            fear_level = launch_wait_sequence(params=params, window=window, image=image, end_time=current_cue_time + CUE_LENGTH,
                                 startles=startle_times, io=io, shock_time=shock_time, fear_level=fear_level)
            timing_index += 1
            print("Leaving a cue")

    return


def wait_with_shocks(window: visual.Window, image: visual.ImageStim, startle_times: list, end_time: time,
                     shock_time: time, io, params, fear_level=5):
    keyboard = io.devices.keyboard
    scale = ratingscale.RatingScale(win=window, scale=None, labels=["0", "10"], low=0, high=10, markerStart=fear_level,
                                    showAccept=False, markerColor="Red", textColor="Black", lineColor="Black",
                                    pos=(0, -window.size[1] / 2 + 200))

    while time.time() <= end_time:

        # Rating Scale
        image.draw()
        scale.draw()
        window.flip()

        # Startles and shocks
        if len(startle_times) == 0:
            pass
        elif startle_times[0] <= time.time() <= startle_times[0] + 0.5:
            helpers.play_startle()
            startle_times.remove(startle_times[0])
        if shock_time <= time.time() <= shock_time + 0.3:
            initiate_shock(params)

        # Escape
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == "escape":
                window.close()
                core.quit()
    print(scale.getRating())
    return scale.getRating()


def wait_without_shocks(window: visual.Window, image: visual.ImageStim, startle_times: list, end_time: time, io,
                        fear_level=5):
    keyboard = io.devices.keyboard
    scale = ratingscale.RatingScale(win=window, scale=None, labels=["0", "10"], low=0, high=10, markerStart=fear_level,
                                    showAccept=False, markerColor="Red", textColor="Black", lineColor="Black",
                                    pos=(0, -window.size[1] / 2 + 200))
    while time.time() <= end_time:

        # Rating Scale
        image.draw()
        scale.draw()
        window.flip()

        # Startles and shocks
        if len(startle_times) == 0:
            pass
        elif startle_times[0] <= time.time() <= startle_times[0] + 0.5:
            helpers.play_startle()
            startle_times.remove(startle_times[0])

        # Escape
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == "escape":
                window.close()
                core.quit()
    print(scale.getRating())
    return scale.getRating()


def launch_wait_sequence(params: dict, window: visual.Window, image: visual.ImageStim, end_time, startles: list, io,
                         shock_time=0, fear_level=5):
    """
    The method prepares the command for launching the wait sequence from the "Helpers" module.
    It takes the cues times, shock times (if there are any) and the end time of the current waiting sequence and organizes
    them into a command.
    """
    startles_filtered = list(filter(lambda cue: time.time() <= cue <= end_time, startles))
    print(f"startles_filtered: {startles_filtered}")
    if shock_time != 0 and time.time() <= shock_time <= end_time:
        print("starting wait with shock")
        fear_level = wait_with_shocks(params=params, window=window, image=image, startle_times=startles_filtered,
                                      end_time=end_time, shock_time=shock_time, io=io, fear_level=fear_level)
    else:
        print("starting wait without shock")
        fear_level = wait_without_shocks(window=window,  image=image, startle_times=startles_filtered,
                                         end_time=end_time, io=io, fear_level=fear_level)
    return fear_level


def initiate_shock(params: dict):
    if params["shockType"] == "Shock":
        # TODO: Add shock mechanism
        pass
    else:
        helpers.play_shock_sound()