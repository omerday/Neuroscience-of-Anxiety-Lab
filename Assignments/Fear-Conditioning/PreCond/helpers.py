from psychopy import visual, core
import time
import dataHadler
from serialHandler import *
from psychopy.iohub.client.keyboard import Keyboard
from psychopy import sound
import psychtoolbox as ptb
import random

STEPS = ["Conditioning", "Test"]
VERSION = ["Short", "Long"]
FACE_COMBINATIONS = [{"CS-": 1, "CS+": 3, "NEW": 10},
                      {"CS-": 1, "CS+": 10, "NEW": 3},
                      {"CS-": 3, "CS+": 1, "NEW": 10},
                      {"CS-": 3, "CS+": 10, "NEW": 1},
                      {"CS-": 10, "CS+": 1, "NEW": 3},
                      {"CS-": 10, "CS+": 3, "NEW": 1}]

def graceful_shutdown(window, params, mood_df):
    dataHadler.export_data(params, Mood=mood_df)
    print(f"Experiment Ended\n===========================================")
    window.close()
    core.quit()
    exit()

def show_slide_and_wait(window, params, df_mood, io, keyboard, image_path, duration, is_space_wait):
    slide = visual.ImageStim(window, image=image_path, units="norm", size=(2, 2))
    slide.draw()
    window.mouseVisible = False
    window.flip()
    start_time = time.time()
    if is_space_wait:
        wait_for_space_and_time(window, params, df_mood, io, start_time, duration)
    else:
        wait_for_time(window, params, df_mood, start_time, duration, keyboard)


def show_blank_slide_and_wait(window, params, df_mood, keyboard, io):
    if params['recordPhysio']:
        report_event(params['serialBiopac'], BIOPAC_EVENTS['blankSlide'])
    show_slide_and_wait(window, params, df_mood, io, keyboard, "./img/blank.jpeg", params['blankSlideDuration'], False)


def wait_for_time(window: visual.Window, params, mood_df, start_time, display_time, keyboard):
    while time.time() < start_time + display_time:
        for event in keyboard.getKeys():
            if event.key == "escape":
                graceful_shutdown(window, params, mood_df)
        core.wait(0.05)

def wait_for_time_with_periodic_events(window: visual.Window, params, mood_df, start_time, display_time, keyboard, prefix, sec):
    while time.time() < start_time + display_time:
        if sec <= time.time() - start_time <= sec + 0.1:
            add_event(params, f'{prefix}_{sec}')
            sec += 2
        for ev in keyboard.getKeys():
            if ev.key == "escape":
                graceful_shutdown(window, params, mood_df)
        core.wait(0.02)

def wait_for_time_with_periodic_events_and_scream(window: visual.Window, params, mood_df, start_time, display_time, keyboard, prefix, sec, soundName: str, volume=.4):
    soundToPlay = sound.Sound(soundName, volume=volume)
    now = ptb.GetSecs()
    soundToPlay.play(when=now)
    while time.time() < start_time + display_time:
        if sec <= time.time() - start_time <= sec + 0.1:
            add_event(params, f'{prefix}_{sec}')
            sec += 2
        for ev in keyboard.getKeys():
            if ev.key == "escape":
                graceful_shutdown(window, params, mood_df)
        core.wait(0.02)
    soundToPlay.stop()


def wait_for_space(window: visual.Window, params, mood_df, io):
    core.wait(0.5)
    keyboard = io.devices.keyboard
    keyboard.getKeys()
    while True:
        for event in keyboard.getKeys():
            if event.key == " ":
                return
            elif event.key == "escape":
                graceful_shutdown(window, params, mood_df)
        core.wait(0.05)

def wait_for_space_and_time(window: visual.Window, params, mood_df, io, start_time, display_time):
    core.wait(0.5)
    keyboard = io.devices.keyboard
    keyboard.getKeys()
    while time.time() < start_time + display_time:
        for event in keyboard.getKeys():
            if event.key == " ":
                return
            elif event.key == "escape":
                graceful_shutdown(window, params, mood_df)
        core.wait(0.05)

def add_event(params: dict, event_name: str):
    event = BIOPAC_EVENTS[event_name]
    report_event(params['serialBiopac'], event)


def show_image_with_scream(window, image_path, sound_path, duration, keyboard, escape_callback, size=(1.5, 2), volume=0.4):
    image_stim = visual.ImageStim(window, image=image_path, units='norm', size=size)
    image_stim.draw()

    sound_to_play = sound.Sound(sound_path, volume=volume)
    next_flip_time = window.getFutureFlipTime(clock='ptb')
    sound_to_play.play(when=next_flip_time)

    window.mouseVisible = False
    window.flip()

    start_time = core.getTime()
    while core.getTime() < start_time + duration:
        for event in keyboard.getKeys():
            if event.key == "escape":
                escape_callback()
        core.wait(0.05)

    sound_to_play.stop()

def generate_test_sequence(repeats_for_each_stimulus: int):
    sequence = ["CS-", "CS+", "NEW"] * repeats_for_each_stimulus
    random.shuffle(sequence)
    while not is_valid(sequence):
        random.shuffle(sequence)
    return sequence

def is_valid(sequence: list):
    for i in range(len(sequence) - 2):
        if sequence[i] == sequence[i + 1] == sequence[i + 2]:
            return False
    return True

