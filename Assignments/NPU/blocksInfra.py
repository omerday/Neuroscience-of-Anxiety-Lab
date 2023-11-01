from psychopy import visual, core, event
import random
import helpers
import time

PATH = "./img/blocks/"
SUFFIX = ".jpg"

BLOCK_LENGTH = 120
CUE_LENGTH = 8
STARTLES_PER_BLOCK = 6

FIXED_CUE_TIMES = [30, 60, 90]


def n_block(window: visual.Window, image: visual.ImageStim, params: dict, io):
    cue_times = randomize_cue_times() if params["timing"] == "Randomized" else FIXED_CUE_TIMES
    startle_times = randomize_startles()
    cue_times, startle_times = prepare_cues_and_startles(cue_times, startle_times)

    timing_index = 0
    start_time = time.time()

    while time.time() < start_time + BLOCK_LENGTH:
        image.image = f"{PATH}N_{params['language'][0]}{SUFFIX}"
        image.setSize((2, 2))
        image.draw()
        window.update()

        launch_wait_sequence(window=window, end_time=start_time + cue_times[timing_index] - 0.5, startles=startle_times, io=io)

        if start_time + cue_times[timing_index] <= time.time() <= start_time + cue_times[timing_index] + 1:
            current_cue_time = time.time()
            image.image = f"{PATH}N_{params['language'][0]}_Cue{SUFFIX}"
            image.setSize((2, 2))
            image.draw()
            window.update()

            launch_wait_sequence(window=window, end_time = time.time() + CUE_LENGTH, startles=startle_times, io=io)

    return


def p_block():
    pass


def u_block():
    pass


def randomize_cue_times():
    random.seed()
    times = [random.randrange(10, 50), random.randrange(30, 90), random.randrange(80, 110)]
    times.sort()

    while times[2] < times[1] + 10:
        times[2] = random.randrange(times[1] + 10, BLOCK_LENGTH - 10)
    while times[1] < times[0] + 10:
        times[1] = random.randrange(times[0] + 10, times[2] - 10)

    return times


def randomize_startles():
    random.seed()
    seconds = list(range(2, 120))
    times = []
    for i in range(STARTLES_PER_BLOCK):
        times.append(random.choice(seconds))
        seconds.remove(times[i])
    times.sort()
    return times


def prepare_cues_and_startles(cues: list, startles: list):
    start_time = time.time()
    cue_times = []
    startle_times = []
    for cue in cues:
        cue_times.append(cue + start_time)
    for startle in startles:
        startle_times.append(startle + start_time)
    return cue_times, startle_times


def launch_wait_sequence(window: visual.Window, end_time, startles: list, io, shock_time=0):
    """
    The method prepares the command for launching the wait sequence from the "Helpers" module.
    It takes the cues times, shock times (if there are any) and the end time of the current waiting sequence and organizes
    them into a command.
    """
    startles_filtered = list(filter(lambda cue: cue <= end_time, startles))
    if shock_time != 0:
        helpers.wait_with_shocks(window=window, cue_times=startles_filtered, end_time=end_time, shock_time=shock_time, io=io)
    else:
        helpers.wait_without_shocks(window=window, cue_times=startles_filtered, end_time=end_time, io=io)