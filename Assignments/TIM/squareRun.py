import time

import pandas as pd
from psychopy import visual, core
from psychopy.iohub.client.keyboard import Keyboard
import random
import VAS
import helpers
from serialHandler import *
from dataHandler import *

T_TO_HEAT = {'T2': 1,
             'T4': 2,
             'T8': 3}

def square_run(window: visual.Window, params: dict, device, io, pain_df: pd.DataFrame, mood_df: pd.DataFrame, block_number: int):
    keyboard = io.devices.keyboard
    repeats = params['nTrials'] // len(params['colors'])
    colors_order = []
    for color in params['colors']:
        for i in range(repeats):
            colors_order.append(color)
    trial = 0
    timings = helpers.create_timing_array(params)
    event_onset_df = setup_fmri_onset_file()
    keyboard = io.devices.keyboard
    helpers.show_waiting_for_next_block(window, params)
    keyboard.getKeys()
    five = False
    while not five:
        for event in keyboard.getKeys():
            if event.key == '5':
                five = True
                break
            elif event.key == 'escape':
                helpers.graceful_shutdown(window, params, device, mood_df, pain_df)
        core.wait(0.05)
    params['fmriStartTime'] = time.time()
    event_onset_df = helpers.add_event(params, 'Start_Cycle', params['fixationBeforeBlock'], 0, event_onset_df)

    helpers.fixation_before_block(window, params, device, mood_df, pain_df, keyboard, event_onset_df)
    while colors_order:
        trial += 1
        trial_timing = timings.pop()
        curr_color = random.choice(colors_order)
        colors_order.remove(curr_color)
        color_index = params['colors'].index(curr_color)
        temperature = params['temps'][color_index]

        # Set the Prefix here
        prefix = params['Ts'][color_index]
        heat_level = T_TO_HEAT[prefix]
        event_onset_df = helpers.add_event(params, f'{prefix}_ITIpre', trial_timing['preITI'], heat_level, event_onset_df)

        helpers.iti(window, params, 'pre', keyboard, device, mood_df, pain_df, trial_timing['preITI'], event_onset_df)

        event_onset_df = helpers.add_event(params, f'{prefix}_{0}', trial_timing['squareOnset'], heat_level, event_onset_df)

        square = visual.ImageStim(window, image=f"./img/squares/{curr_color}_{2}.jpeg", units="norm", size=(2,2))
        square.draw()
        # Show Square
        window.mouseVisible = False
        window.flip()
        start_time = time.time()
        sec = 2
        sec, event_onset_df = helpers.wait_for_time_with_periodic_events(window, params, device, mood_df, pain_df, start_time, trial_timing['squareOnset'], keyboard, prefix, sec, event_onset_df)
        # Remove square from the screen
        square.image = "./img/squares/blank.jpg"
        square.draw()
        window.mouseVisible = False
        window.flip()
        blank_screen_time = trial_timing['squareBlankScreen'] + trial_timing['squareJitter']
        if time.time() > start_time + 2.1:
            sec = 4
        _, event_onset_df = helpers.wait_for_time_with_periodic_events(window, params, device, mood_df, pain_df, start_time, blank_screen_time, keyboard, prefix, sec, event_onset_df)

        if params['painSupport']:
            import heatHandler
            event_onset_df = helpers.add_event(params, f'{prefix}_heat_pulse', 6, heat_level, event_onset_df)
            heatHandler.deliver_pain(window, float(temperature), device, params)

        helpers.iti(window, params, "post", keyboard, device, mood_df, pain_df, trial_timing['preRatingITI'], event_onset_df)

        event_onset_df = helpers.add_event(params, f'{prefix}_PainRatingScale', params['painRateDuration'], heat_level, event_onset_df)

        pain = VAS.run_vas(window, io, params, "PainRating", duration=trial_timing['painRating'], mood_df=mood_df, pain_df=pain_df, device=device)
        pain_df = insert_data_pain(block_number, trial, (color_index + 1), curr_color, pain, pain_df)

        event_onset_df = helpers.add_event(params, f'{prefix}_ITIpost', trial_timing['postITI'], heat_level, event_onset_df)
        helpers.iti(window, params, 'post', keyboard, device, mood_df, pain_df, trial_timing['postITI'], event_onset_df)

        helpers.save_backup(params, Mood=mood_df, Pain=pain_df)
        helpers.save_fmri_event_onset(params, event_onset_df, block_number)
    return pain_df



