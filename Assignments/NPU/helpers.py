from psychopy import visual, core, event
from psychopy.iohub import launchHubServer
from psychopy.iohub.client.keyboard import Keyboard
from psychopy.visual import ratingscale
from psychopy import sound
import psychtoolbox as ptb
import time
import random

from Assignments.NPU import blocksInfra


def wait_for_space(window: visual.Window, io):
    keyboard = io.devices.keyboard
    while True:
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == " ":
                return
            if event.key == "escape":
                window.close()
                core.quit()


def wait_for_space_with_replay(window, io):
    keyboard = io.devices.keyboard
    while True:
        keys = keyboard.getPresses()
        for event in keys:
            if event.key == 'r' or event.key == 'R':
                return True
            elif event.key == ' ':
                return False
            elif event.key == "escape":
                window.close()
                core.quit()


def wait_for_space_with_rating_scale(window, img: visual.ImageStim, io, params:dict):
    keyboard = io.devices.keyboard
    print(-params["screenSize"][1]/2 + 100)
    scale = ratingscale.RatingScale(win=window, scale=None,labels=["0", "10"], low=0, high=10, markerStart=5, showAccept=False, markerColor="Red",
                                   acceptKeys=["space"], textColor="Black", lineColor="Black", pos=(0,-window.size[1]/2 + 200))
    while scale.noResponse:
        img.draw()
        scale.draw()
        window.flip()


def play_startle_and_wait(window: visual.Window, io):
    soundToPlay = sound.Sound("./sounds/startle_probe.wav")
    core.wait(2)
    now = ptb.GetSecs()
    soundToPlay.play(when=now)
    core.wait(1)
    keyboard = io.devices.keyboard
    while True:
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == " ":
                soundToPlay.stop()
                return
            if event.key == "escape":
                window.close()
                core.quit()


def randomize_cue_times():
    random.seed()
    times = [random.randrange(10, 50), random.randrange(30, 90), random.randrange(80, 110)]
    times.sort()

    while times[2] < times[1] + 10:
        times[2] = random.randrange(times[1] + 10, blocksInfra.BLOCK_LENGTH - 10)
    while times[1] < times[0] + 10:
        times[1] = random.randrange(times[0] + 10, times[2] - 10)

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
        chosen_sec = random.choice(seconds)
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


def play_startle():
    soundToPlay = sound.Sound("./sounds/startle_probe.wav")
    now = ptb.GetSecs()
    soundToPlay.play(when=now)
    core.wait(1)


def play_shock_sound():
    soundToPlay = sound.Sound("./sounds/shock_sound.mp3")
    now = ptb.GetSecs()
    soundToPlay.play(when=now)
    core.wait(1.5)
