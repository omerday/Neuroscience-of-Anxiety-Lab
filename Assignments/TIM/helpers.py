import time
from psychopy import visual, core
from psychopy.iohub.client.keyboard import Keyboard
import random
import serial, serialHandler
import VAS
from Assignments.NPU.SoundSequences import event
from dataHandler import *
from serialHandler import *

PRE_BLOCK_FIXATION_TIME = 8


def iti(window: visual.Window, params: dict, iti_type, keyboard, device, mood_df, pain_df, display_time, event_onset_df=None):
    # display_time = random.uniform(params[f'{iti_type}ITIMin'], params[f'{iti_type}ITIMax'])
    image = "./img/blank.jpeg" if iti_type == "post" else "./img/plus.jpeg"
    square = visual.ImageStim(window, image=image, units="norm", size=(2, 2))
    square.draw()
    window.mouseVisible = False
    window.flip()
    start_time = time.time()
    wait_for_time(window, params, device, mood_df, pain_df, start_time, display_time, keyboard, event_onset_df)


def wait_for_RA(window, params, device, mood_df, pain_df, io):
    image_path = f"./img/waitForRA_{'E' if params['language'] == 'English' else params['gender'][0]}.jpeg"
    image = visual.ImageStim(window, image=image_path, units="norm", size=(2, 2))
    image.draw()
    window.mouseVisible = False
    window.flip()
    wait_for_space(window, params, device, mood_df, pain_df, io)


def wait_for_time(window: visual.Window, params, device, mood_df, pain_df, start_time, display_time, keyboard, event_onset_df=None):
    while time.time() < start_time + display_time:
        for event in keyboard.getKeys():
            if event.key == "escape":
                graceful_shutdown(window, params, device, mood_df, pain_df, event_onset_df)
        core.wait(0.05)

def fixation_before_block(window:visual.Window, params, device, mood_df, pain_df, keyboard, event_onset_df=None):
    image = visual.ImageStim(window, f"./img/plus.jpeg", units="norm", size=(2,2))
    image.draw()
    window.mouseVisible = False
    window.flip()
    wait_for_time(window, params, device, mood_df, pain_df, time.time(), params['fixationBeforeBlock'], keyboard, event_onset_df)

def wait_for_time_with_periodic_events(window: visual.Window, params, device, mood_df, pain_df, start_time, display_time, keyboard, prefix, sec, event_onset_df: pd.DataFrame):
    while time.time() < start_time + display_time:
        if sec <= time.time() - start_time <= sec + 0.1:
            event = PARADIGM_2_BIOPAC_EVENTS[f'{prefix}_{sec}']
            event_onset_df = add_event(params, event, 2, event_onset_df)
            report_event(params['serialBiopac'], PARADIGM_2_BIOPAC_EVENTS[f'{prefix}_{sec}'])
            sec += 2
        for ev in keyboard.getKeys():
            if ev.key == "escape":
                graceful_shutdown(window, params, device, mood_df, pain_df, event_onset_df)
        core.wait(0.02)
    return sec, event_onset_df


def wait_for_space(window: visual.Window, params, device, mood_df, pain_df, io, event_onset_df=None):
    keyboard = io.devices.keyboard
    keyboard.getKeys()
    core.wait(0.1)
    while True:
        for event in keyboard.getKeys():
            if event.key == " ":
                return
            elif event.key == "escape":
                graceful_shutdown(window, params, device, mood_df, pain_df, event_onset_df)
        core.wait(0.05)


def graceful_shutdown(window, params, device, mood_df, pain_df, event_onset_df=None):
    if params['painSupport']:
        from heatHandler import cool_down
        cool_down(device)
    export_data(params, Mood=mood_df, Pain=pain_df)
    save_fmri_event_onset(params, event_onset_df, "backup")
    print(f"Experiment Ended\n===========================================")
    window.close()
    core.quit()
    exit()


def show_waiting_for_next_block(window: visual.Window, params: dict, ):
    image = visual.ImageStim(window, f"./img/wait_E.jpeg" if params['language'] == 'English' else f"./img/wait_{params['gender'][0]}.jpeg", units="norm", size=(2, 2))
    image.draw()
    window.flip()

def create_timing_array(params):
    random.seed(time.time())
    while True:
        timings = []
        for i in range(params['nTrials']):
            timing_dict = {
                'preITI': random.uniform(params['preITIMin'], params['preITIMax']),
                'squareOnset': params['secondParadigmSquareOnset'],
                'squareBlankScreen': params['secondParadigmSquareBlankScreen'],
                'squareJitter': random.uniform(params['secondParadigmJitterMin'], params['secondParadigmJitterMax']),
                'painTime': 6,
                'preRatingITI': params['preRatingITI'],
                'painRating': params['painRateDuration'],
                'postITI': random.uniform(params['postITIMin'], params['postITIMax']),
            }
            timings.append(timing_dict)
        timings_sum = sum_timing_array(timings) + PRE_BLOCK_FIXATION_TIME
        print(f"Timing Sum = {timings_sum}\n==================================")
        if timings_sum <= 240:
            return timings


def sum_timing_array(timings: list):
    time_sum = 0
    for timing_dict in timings:
        time_sum += sum(timing_dict.values())
    return time_sum

def add_event(params: dict, event_name: str, event_time, event_onset_file: pd.DataFrame):
    event = PARADIGM_2_BIOPAC_EVENTS[event_name]
    report_event(params['serialBiopac'], event)
    return insert_data_fmri_events(params, event, event_time, event_onset_file)