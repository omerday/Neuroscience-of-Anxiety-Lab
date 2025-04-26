from psychopy import visual, core
import time
import dataHadler
from serialHandler import *
from psychopy.iohub.client.keyboard import Keyboard
from psychopy import sound
import psychtoolbox as ptb

def graceful_shutdown(window, params, mood_df):
    dataHadler.export_data(params, Mood=mood_df)
    print(f"Experiment Ended\n===========================================")
    window.close()
    core.quit()
    exit()

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


def wait_for_time_and_play_sound(window: visual.Window, params, mood_df, start_time, display_time, keyboard, soundName: str, volume=.4):
    soundToPlay = sound.Sound(soundName, volume=volume)
    # Synchronize sounds with next screen flip
    next_flip_time = window.getFutureFlipTime(clock="now")
    soundToPlay.play(when=next_flip_time)
    """
    now = ptb.GetSecs()
    soundToPlay.play(when=now)
    """
    while time.time() < start_time + display_time:
            for event in keyboard.getKeys():
                if event.key == "escape":
                    graceful_shutdown(window, params, mood_df)
            core.wait(0.05)
    soundToPlay.stop()


