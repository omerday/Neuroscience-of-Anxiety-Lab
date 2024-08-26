import time
from psychopy import visual, core
from psychopy.iohub.client.keyboard import Keyboard
import random
import serial, serialHandler
import VAS
from dataHandler import *
from serialHandler import *


def iti(window: visual.Window, params: dict, iti_type, keyboard, device, mood_df, pain_df):
    display_time = random.uniform(params[f'{iti_type}ITIMin'], params[f'{iti_type}ITIMax'])
    image = "./img/blank.jpeg" if iti_type == "post" else "./img/plus.jpeg"
    square = visual.ImageStim(window, image=image, units="norm", size=(2, 2))
    square.draw()
    window.mouseVisible = False
    window.flip()
    start_time = time.time()
    wait_for_time(window, params, device, mood_df, pain_df, start_time, display_time, keyboard)


def wait_for_RA(window, params, device, mood_df, pain_df, io):
    image_path = f"./img/waitForRA_{'E' if params['language'] == 'English' else params['gender'][0]}.jpeg"
    image = visual.ImageStim(window, image=image_path, units="norm", size=(2, 2))
    image.draw()
    window.mouseVisible = False
    window.flip()
    wait_for_space(window, params, device, mood_df, pain_df, io)


def wait_for_time(window: visual.Window, params, device, mood_df, pain_df, start_time, display_time, keyboard):
    while time.time() < start_time + display_time:
        for event in keyboard.getKeys():
            if event.key == "escape":
                graceful_shutdown(window, params, device, mood_df, pain_df)
        core.wait(0.05)


def wait_for_time_2(window: visual.Window, params, device, mood_df, pain_df, start_time, display_time, keyboard, prefix, sec):
    while time.time() < start_time + display_time:
        if sec <= time.time() - start_time <= sec + 0.1:
            report_event(params['serialBiopac'], PARADIGM_2_BIOPAC_EVENTS[f'{prefix}_{sec}'])
            sec += 2
        for event in keyboard.getKeys():
            if event.key == "escape":
                graceful_shutdown(window, params, device, mood_df, pain_df)
        core.wait(0.02)
    return sec


def wait_for_space(window: visual.Window, params, device, mood_df, pain_df, io):
    keyboard = io.devices.keyboard
    keyboard.getKeys()
    core.wait(0.1)
    while True:
        for event in keyboard.getKeys():
            if event.key == " ":
                return
            elif event.key == "escape":
                graceful_shutdown(window, params, device, mood_df, pain_df)
        core.wait(0.05)


def graceful_shutdown(window, params, device, mood_df, pain_df):
    if params['painSupport']:
        from heatHandler import cool_down
        cool_down(device)
    export_data(params, Mood=mood_df, Pain=pain_df)
    print(f"Experiment Ended\n===========================================")
    window.close()
    core.quit()
    exit()


def show_waiting_for_next_block(window: visual.Window, params: dict, ):
    image = visual.ImageStim(window, f"./img/wait_E.jpeg" if params['language'] == 'English' else f"./img/wait_{params['gender'][0]}.jpeg", units="norm", size=(2, 2))
    image.draw()
    window.flip()
