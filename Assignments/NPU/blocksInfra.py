from psychopy import visual, core, event
import random
import helpers
import time
from psychopy.iohub.client.keyboard import Keyboard

PATH = "./img/blocks/"
SUFFIX = ".jpg"

BLOCK_LENGTH = 120
CUE_LENGTH = 8
STARTLES_PER_BLOCK = 6

FIXED_CUE_TIMES = [30, 60, 90]


def n_block(window: visual.Window, image: visual.ImageStim, params: dict, io):
    cue_times = helpers.randomize_cue_times()
    if not params["skipStartle"]:
        startle_times = helpers.randomize_startles(cue_times)
    else:
        startle_times = []
    cue_times, startle_times = helpers.prepare_cues_and_startles(cue_times, startle_times)

    timing_index = 0
    start_time = time.time()

    while time.time() < start_time + BLOCK_LENGTH:
        image.image = f"{PATH}N_{params['language'][0]}{SUFFIX}"
        image.setSize((2, 2))
        image.draw()
        window.update()

        launch_wait_sequence(window=window, end_time=cue_times[timing_index] - 0.5, startles=startle_times, io=io)

        if cue_times[timing_index] <= time.time() <= cue_times[timing_index] + 1:
            current_cue_time = time.time()
            image.image = f"{PATH}N_{params['language'][0]}_Cue{SUFFIX}"
            image.setSize((2, 2))
            image.draw()
            window.update()

            launch_wait_sequence(window=window, end_time = current_cue_time + CUE_LENGTH, startles=startle_times, io=io)

    return


def p_block():
    pass


def u_block():
    pass


def wait_with_shocks(window: visual.Window, cue_times: list, end_time: time, shock_time: time, io):
    pass


def wait_without_shocks(window: visual.Window, cue_times: list, end_time: time, io):
    keyboard = io.devices.keyboard
    while time.time() <= end_time:
        if len(cue_times) == 0:
            pass
        elif cue_times[0] <= time.time() <= cue_times[0] + 0.5:
            helpers.play_startle()
            cue_times.remove(cue_times[0])

        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == "escape":
                window.close()
                core.quit()


def launch_wait_sequence(window: visual.Window, end_time, startles: list, io, shock_time=0):
    """
    The method prepares the command for launching the wait sequence from the "Helpers" module.
    It takes the cues times, shock times (if there are any) and the end time of the current waiting sequence and organizes
    them into a command.
    """
    startles_filtered = list(filter(lambda cue: cue <= end_time, startles))
    if shock_time != 0:
        wait_with_shocks(window=window, cue_times=startles_filtered, end_time=end_time, shock_time=shock_time, io=io)
    else:
        wait_without_shocks(window=window, cue_times=startles_filtered, end_time=end_time, io=io)