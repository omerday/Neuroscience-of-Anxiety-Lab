import random
import time

import pandas as pd
from psychopy import visual

import helpers


def test(params, window: visual.Window, io, keyboard, df_mood: pd.DataFrame):
    for i in range(3):
        temp_naturals = []
        for N in params['natural']:
            temp_naturals.append(N)

        while temp_naturals:
            # choosing natural face
            neut_img_name = random.choice(temp_naturals)
            prefix = neut_img_name.split('_')[0]  # for the events
            temp_naturals.remove(neut_img_name)
            # img_name = params['natural'].index(curr_n)

            """ 
            # displaying the plus image before the shape
            display_time_plus = random.uniform(params['plusDurationMin'], params['plusDurationMax'])
            plus = visual.ImageStim(window, image=f"./img/plus.jpeg", units="norm", size=(2, 2))
            plus.draw()
            window.mouseVisible = False
            window.flip()
            start_time = time.time()
            helpers.add_event(params, f'{prefix}_plus')
            helpers.wait_for_time(window, params, df_mood, start_time, display_time_plus, keyboard)
            """

            # displaying the natural face
            display_time_n = random.uniform(params['faceDurationMin'], params['faceDurationMax'])
            shape = visual.ImageStim(window, image=f"./img/Natural/{neut_img_name}.jpeg", units="norm", size=(2, 2))
            shape.draw()
            window.mouseVisible = False
            window.flip()
            start_time = time.time()
            # adding event every 2 sec
            helpers.wait_for_time_with_periodic_events(window, params, df_mood, start_time, display_time_n, keyboard, prefix, 0)

            # ITI
            display_time_iti = params["testBlockDuration"] - display_time_n
            blank = visual.ImageStim(window, image=f"./img/blank.jpeg", units="norm", size=(2, 2))
            blank.draw()
            window.mouseVisible = False
            window.flip()
            start_time = time.time()
            # adding event when starting ITI
            helpers.add_event(params, f'{prefix}_ITIpre')
            helpers.wait_for_time(window, params, df_mood, start_time, display_time_iti, keyboard)
            # adding event after ITI
            helpers.add_event(params, f'{prefix}_ITIpost')