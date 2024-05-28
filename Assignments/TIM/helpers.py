import time
from psychopy import visual, core
from psychopy.iohub.client.keyboard import Keyboard
import random
import serial, serialHandler
import VAS
from dataHandler import *


def iti(window: visual.Window, params: dict, iti_type, keyboard, device, mood_df, pain_df):
    display_time = random.uniform(params[f'{iti_type}ITIMin'], params[f'{iti_type}ITIMax'])
    image = "./img/blank.jpeg" if iti_type == "post" else "./img/plus.jpeg"
    square = visual.ImageStim(window, image=image, units="norm", size=(2, 2))
    square.draw()
    window.flip()
    start_time = time.time()
    wait_for_time(window, params, device, mood_df, pain_df, start_time, display_time, keyboard)


def wait_for_time(window: visual.Window, params, device, mood_df, pain_df, start_time, display_time, keyboard):
    while time.time() < start_time + display_time:
        for event in keyboard.getKeys():
            if event.key == "escape":
                graceful_shutdown(window, params, device, mood_df, pain_df)
        core.wait(0.05)


def wait_for_space(window: visual.Window, params, device, mood_df, pain_df, io):
    keyboard = io.devices.keyboard
    while True:
        for event in keyboard.getKeys():
            if event.key == "space":
                return
            elif event.key == "escape":
                graceful_shutdown(window, params, device, mood_df, pain_df)
        core.wait(0.05)


def graceful_shutdown(window, params, device, mood_df, pain_df):
    if params['painSupport']:
        from heatHandler import cool_down
        cool_down(device)
    export_data(params, Mood=mood_df, Pain=pain_df)
    window.close()
    core.quit()
    exit()
