from psychopy import visual, core
import time
import dataHadler
from psychopy.iohub.client.keyboard import Keyboard

def graceful_shutdown(window, params, mood_df):
    dataHadler.export_data(params, Mood=mood_df)
    print(f"Experiment Ended\n===========================================")
    window.close()
    core.quit()
    exit()

def wait_for_time(window: visual.Window, params, start_time, display_time, keyboard):
    while time.time() < start_time + display_time:
        for event in keyboard.getKeys():
            if event.key == "escape":
                graceful_shutdown(window, params)
        core.wait(0.05)

def wait_for_space(window: visual.Window, params, mood_df, io):
    keyboard = io.devices.keyboard
    keyboard.getKeys()
    core.wait(0.1)
    while True:
        for event in keyboard.getKeys():
            if event.key == " ":
                return
            elif event.key == "escape":
                graceful_shutdown(window, params, mood_df)
        core.wait(0.05)