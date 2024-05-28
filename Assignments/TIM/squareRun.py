import time

import pandas as pd
from psychopy import visual, core
from psychopy.iohub.client.keyboard import Keyboard
import random
import VAS
import helpers
from serialHandler import *
from dataHandler import *


def square_run(window: visual.Window, params: dict, device, io, pain_df: pd.DataFrame, mood_df: pd.DataFrame, nBlock: int):
    keyboard = io.devices.keyboard
    repeats = params['nTrials'] // len(params['colors'])
    colors_order = []
    for color in params['colors']:
        for i in range(repeats):
            colors_order.append(color)
    trail = 0
    while colors_order:
        trail += 1
        curr_color = random.choice(colors_order)
        colors_order.remove(curr_color)
        color_index = params['colors'].index(curr_color)
        temperature = params['temps'][color_index]
        # Set the Prefix here
        prefix = params['Ts'][color_index]
        if params['recordPhysio']:
            report_event(params['serialBiopac'], BIOPAC_EVENTS[f'{prefix}_ITIpre'])
        helpers.iti(window, params, 'pre', keyboard)
        if params['paradigm'] == 1:
            for i in range(1, 6):
                if params['recordPhysio']:
                    report_event(params['serialBiopac'], BIOPAC_EVENTS[f'{prefix}_square{i}'])
                display_time = random.uniform(params['squareDurationMin'], params['squareDurationMax'])
                square = visual.ImageStim(window, image=f"./img/squares/{curr_color}_{i}.jpeg", units="norm", size=(2,2))
                square.draw()
                window.flip()
                start_time = time.time()
                if params['continuousShape'] or i == 5:
                    helpers.wait_for_time(window, start_time, display_time, keyboard)
                else:
                    present_time = random.uniform(params['continuousPresentTimeMin'],params['continuousPresentTimeMax'])
                    helpers.wait_for_time(window, start_time, present_time, keyboard)
                    square.image = "./img/squares/blank.jpg"
                    square.draw()
                    window.flip()
                    helpers.wait_for_time(window, start_time, display_time, keyboard)

        else:
            display_time = random.uniform(params['secondParadigmMin'], params['secondParadigmMax'])
            square = visual.ImageStim(window, image=f"./img/squares/{curr_color}_{3}.jpeg", units="norm", size=(2,2))
            square.draw()
            window.flip()
            start_time = time.time()
            helpers.wait_for_time(window, start_time, display_time, keyboard)

        if params['painSupport']:
            import heatHandler
            if params['recordPhysio']:
                report_event(params['serialBiopac'], BIOPAC_EVENTS[f'{prefix}_heat_pulse'])
            heatHandler.deliver_pain(window, float(temperature), device)

        if params['recordPhysio']:
            report_event(params['serialBiopac'], BIOPAC_EVENTS[f'{prefix}_PainRatingScale'])
        pain = VAS.run_vas(window, io, params, "PainRating", params['painRateDuration'])
        pain_df = insert_data_pain(nBlock, trail, (color_index+1), curr_color, pain, pain_df)

        if params['recordPhysio']:
            report_event(params['serialBiopac'], BIOPAC_EVENTS[f'{prefix}_ITIpost'])
        helpers.iti(window, params, 'post', keyboard)

    return pain_df



