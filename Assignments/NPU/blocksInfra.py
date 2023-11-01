from psychopy import visual, core, event
import random
import time

PATH = "./img/blocks/"
SUFFIX = ".jpg"

BLOCK_LENGTH = 120
CUE_LENGTH = 8
STARTLES_PER_BLOCK = 6

FIXED_CUE_TIMES = [30, 60, 90]


def n_block(window: visual.Window, image: visual.ImageStim, params: dict, io):
    cue_times = randomize_cue_times() if params["timing"] else FIXED_CUE_TIMES
    timing_index = 0
    start_time = time.time()
    image.image = f"{PATH}N_{params['language'][0]}{SUFFIX}"
    image.setSize((2, 2))
    image.draw()
    window.update()
    while time.time() < start_time + BLOCK_LENGTH:
        # TODO: Write to DF
        if start_time + cue_times[timing_index] <= time.time() <= start_time + cue_times[timing_index] + 1:
            current_cue_time = time.time()
            image.image = f"{PATH}N_{params['language'][0]}_Cue{SUFFIX}"
            image.setSize((2, 2))
            image.draw()
            window.update()
            while time.time() < current_cue_time + CUE_LENGTH:
                # TODO: Write to DF
                pass
            image.image = f"{PATH}N_{params['language'][0]}{SUFFIX}"
            image.setSize((2, 2))
            image.draw()
            window.update()
            timing_index += 1
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
