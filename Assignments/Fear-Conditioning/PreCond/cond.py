import random
import time

import pandas as pd
from psychopy import visual
import helpers


def pre_cond(params, window: visual.Window, io, keyboard, df_mood: pd.DataFrame):
    temp_naturals = []
    for N in params['natural']:
        temp_naturals.append(N)

    prev_gender = ""
    counter = 1
    while temp_naturals:
        # choosing shape
        curr_img = random.choice(temp_naturals)
        img_name = params['natural'].index(curr_img)
        angry_img_name = params['angry'].index(curr_img)
        if 'F' in img_name:
            if prev_gender == 'F':
                counter += 1
            prev_gender = "F"
        elif 'M' in img_name:
            if prev_gender == 'M':
                counter += 1
            prev_gender = "M"
        else:
            counter = 1

        if counter != 4:
            prefix = curr_img.split('_')[0] # for the events
            temp_naturals.remove(curr_img)
            display_time_img_angry = 0

            # displaying the plus image before the shape
            display_time_plus = random.uniform(params['plusDurationMin'], params['plusDurationMax'])
            plus = visual.ImageStim(window, image=f"./img/plus.jpeg", units="norm", size=(2, 2))
            plus.draw()
            window.mouseVisible = False
            window.flip()
            start_time = time.time()
            # TODO: add event
            helpers.wait_for_time(window, params, start_time, display_time_plus, keyboard, df_mood)

            # displaying the img
            display_time_img = random.uniform(params['faceDurationMin'], params['faceDurationMax'])
            img = visual.ImageStim(window, image=f"./img/Natural/{img_name}.jpg", units="norm", size=(2, 2))
            img.draw()
            window.mouseVisible = False
            window.flip()
            start_time = time.time()
            # TODO: add event every 2 sec
            # helpers.wait_for_time_with_periodic_events(window, params, mood_df, start_time, display_time_img, keyboard, prefix, 0)
            helpers.wait_for_time(window, params, start_time, display_time_img, keyboard, df_mood)

            if len(temp_naturals) == 4:
                display_time_img_angry = 2
                angry_img = visual.ImageStim(window, image=f"./img/Angry/{angry_img_name}.jpg", units="norm", size=(2, 2))
                angry_img.draw()
                # TODO: צעקה
                window.mouseVisible = False
                window.flip()
                start_time = time.time()
                # TODO: add event
                helpers.wait_for_time(window, params, start_time, display_time_img_angry, keyboard, df_mood)

            # ITI
            display_time_iti = params["blockDuration"] - display_time_img - display_time_plus - display_time_img_angry
            blank = visual.ImageStim(window, image=f"./img/blank.jpeg", units="norm", size=(2, 2))
            blank.draw()
            window.mouseVisible = False
            window.flip()
            start_time = time.time()
            # TODO: add event when starting ITI
            helpers.wait_for_time(window, params, start_time, display_time_iti, keyboard, df_mood)
            # TODO: add event after ITI