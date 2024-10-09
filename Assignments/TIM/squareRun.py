import time

import pandas as pd
from psychopy import visual, core
from psychopy.iohub.client.keyboard import Keyboard
import random
import VAS
import helpers
from Assignments.TIM.helpers import fixation_before_block
from serialHandler import *
from dataHandler import *


def square_run(window: visual.Window, params: dict, device, io, pain_df: pd.DataFrame, mood_df: pd.DataFrame, nBlock: int):
    keyboard = io.devices.keyboard
    repeats = params['nTrials'] // len(params['colors'])
    colors_order = []
    for color in params['colors']:
        for i in range(repeats):
            colors_order.append(color)
    trial = 0
    timings = helpers.create_timing_array(params)
    if params['fmriVersion']:
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
        params['fmriStartTime'] = time.time()
        fixation_before_block(window, params, device, mood_df, pain_df, keyboard)
    while colors_order:
        trial += 1
        trial_timing = timings.pop()
        curr_color = random.choice(colors_order)
        colors_order.remove(curr_color)
        color_index = params['colors'].index(curr_color)
        temperature = params['temps'][color_index]
        # Set the Prefix here
        prefix = params['Ts'][color_index]

        report_event(params['serialBiopac'], BIOPAC_EVENTS[f'{prefix}_ITIpre'])
        helpers.iti(window, params, 'pre', keyboard, device, mood_df, pain_df, trial_timing['preITI'])
        if params['paradigm'] == 1:
            for i in range(1, 6):
                if params['recordPhysio']:
                    report_event(params['serialBiopac'], BIOPAC_EVENTS[f'{prefix}_square{i}'])
                display_time = random.uniform(params['squareDurationMin'], params['squareDurationMax'])
                square = visual.ImageStim(window, image=f"./img/squares/{curr_color}_{i}.jpeg", units="norm", size=(2,2))
                square.draw()
                window.mouseVisible = False
                window.flip()
                start_time = time.time()
                if params['continuousShape'] or i == 5:
                    helpers.wait_for_time(window, params, device, mood_df, pain_df, start_time, display_time, keyboard)
                else:
                    present_time = random.uniform(params['continuousPresentTimeMin'],params['continuousPresentTimeMax'])
                    helpers.wait_for_time(window, params, device, mood_df, pain_df, start_time, present_time, keyboard)
                    square.image = "./img/squares/blank.jpg"
                    square.draw()
                    window.mouseVisible = False
                    window.flip()
                    helpers.wait_for_time(window, params, device, mood_df, pain_df, start_time, display_time, keyboard)

        else:
            report_event(params['serialBiopac'], PARADIGM_2_BIOPAC_EVENTS[f'{prefix}_{0}'])
            display_time = random.uniform(params['secondParadigmMin'], params['secondParadigmMax'] - 0.01)
            square = visual.ImageStim(window, image=f"./img/squares/{curr_color}_{2}.jpeg", units="norm", size=(2,2))
            square.draw()
            # Show Square
            window.mouseVisible = False
            window.flip()
            start_time = time.time()
            sec = 2
            sec = helpers.wait_for_time_2(window, params, device, mood_df, pain_df, start_time, trial_timing['squareOnset'], keyboard, prefix, sec)
            # Remove square from the screen
            square.image = "./img/squares/blank.jpg"
            square.draw()
            window.mouseVisible = False
            window.flip()
            blank_screen_time = trial_timing['squareBlankScreen'] + trial_timing['squareJitter']
            helpers.wait_for_time_2(window, params, device, mood_df, pain_df, start_time, blank_screen_time , keyboard, prefix, sec)

        if params['painSupport']:
            import heatHandler
            report_event(params['serialBiopac'], BIOPAC_EVENTS[f'{prefix}_heat_pulse'])
            heatHandler.deliver_pain(window, float(temperature), device)

        report_event(params['serialBiopac'], BIOPAC_EVENTS[f'{prefix}_PainRatingScale'])
        pain = VAS.run_vas(window, io, params, "PainRating", duration=trial_timing['painRating'], mood_df=mood_df, pain_df=pain_df, device=device)
        pain_df = insert_data_pain(nBlock, trial, (color_index+1), curr_color, pain, pain_df)

        report_event(params['serialBiopac'], BIOPAC_EVENTS[f'{prefix}_ITIpost'])
        helpers.iti(window, params, 'post', keyboard, device, mood_df, pain_df, trial_timing['postITI'])

        helpers.save_backup(params, Mood=mood_df, Pain=pain_df)

    return pain_df



