import random
import time

import pandas as pd
from psychopy import visual
import helpers


def cond(params, window: visual.Window, io, keyboard, df_mood: pd.DataFrame):
    temp_naturals = []
    for N in params['natural']:
        temp_naturals.append(N)

    prev_gender = ""
    counter = 1
    while temp_naturals:
        # choosing img
        neut_img_name = random.choice(temp_naturals)
        # img_name = params['natural'].index(curr_img)
        angry_img_name = f'A{neut_img_name[1:]}'
        if 'F' in neut_img_name:
            if prev_gender == 'F':
                counter += 1
            prev_gender = "F"
        elif 'M' in neut_img_name:
            if prev_gender == 'M':
                counter += 1
            prev_gender = "M"
        else:
            counter = 1

        if counter != 4:
            prefix = neut_img_name.split('_')[0] # for the events
            temp_naturals.remove(neut_img_name)

            # displaying the plus image before the shape
            display_time_plus = random.uniform(params['plusDurationMin'], params['plusDurationMax'])
            plus = visual.ImageStim(window, image=f"./img/plus.jpeg", units="norm", size=(2, 2))
            plus.draw()
            window.mouseVisible = False
            window.flip()
            start_time = time.time()
            # plus add event
            helpers.add_event(params, f'{prefix}_plus')
            helpers.wait_for_time(window, params, df_mood, start_time, display_time_plus, keyboard)

            # displaying the img
            display_time_img = random.uniform(params['faceDurationMin'], params['faceDurationMax'])
            img = visual.ImageStim(window, image=f"./img/Natural/{neut_img_name}.jpg", units="norm", size=(2, 2))
            img.draw()
            window.mouseVisible = False
            window.flip()
            start_time = time.time()
            # add event every 2 sec
            helpers.wait_for_time_with_periodic_events(window, params, df_mood, start_time, display_time_img, keyboard, prefix, 0)
            # helpers.wait_for_time(window, params, start_time, display_time_img, keyboard, df_mood)

            display_time_img_angry = 2
            if len(temp_naturals) == 4:
                angry_img = visual.ImageStim(window, image=f"./img/Angry/{angry_img_name}.jpg", units="norm", size=(2, 2))
                angry_img.draw()
                window.mouseVisible = False
                window.flip()
                start_time = time.time()
                helpers.wait_for_time_and_play_sound(window, params, df_mood, start_time, display_time_img_angry, keyboard, "./sounds/scream.wav", volume=.4)
                helpers.add_event(params, f'{prefix}_angry')

            # ITI
            display_time_iti = params["blockDuration"] - display_time_img - display_time_plus - display_time_img_angry
            blank = visual.ImageStim(window, image=f"./img/blank.jpeg", units="norm", size=(2, 2))
            blank.draw()
            window.mouseVisible = False
            window.flip()
            start_time = time.time()
            # TODO: add event when starting ITI
            helpers.add_event(params, f'{prefix}_ITIpre')
            helpers.wait_for_time(window, params, df_mood, start_time, display_time_iti, keyboard)
            # TODO: add event after ITI
            helpers.add_event(params, f'{prefix}_ITIpost')