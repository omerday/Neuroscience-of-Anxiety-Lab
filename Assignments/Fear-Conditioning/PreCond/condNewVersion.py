import random
import time

import pandas as pd
from psychopy import visual
import helpers


def cond_new_version(params, window: visual.Window, io, keyboard, df_mood: pd.DataFrame):
    temp_naturals = []
    if params['gender'] == 'Female':
        for N in params['N_F_newVersion']:
            temp_naturals.append(N)
    else:
        for N in params['N_M_newVersion']:
            temp_naturals.append(N)

    prev_img = ""
    counter = 1
    while temp_naturals:
        # choosing img
        neut_img_name = random.choice(temp_naturals)
        angry_img_name = f'A{neut_img_name[1:]}'
        if prev_img == neut_img_name:
            counter += 1
        else:
            counter = 1
        prev_img = neut_img_name

        if counter != 3:
            prefix = neut_img_name.split('_')[0] # for the events
            temp_naturals.remove(neut_img_name)

            """"
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
            """

            # displaying the img
            display_time_img = random.uniform(params['faceDurationMin'], params['faceDurationMax'])
            img = visual.ImageStim(window, image=f"./img/Natural/{neut_img_name}.jpg", units="norm", size=(1.5, 1.5))
            img.draw()
            window.mouseVisible = False
            window.flip()
            start_time = time.time()
            # add event every 2 sec
            helpers.wait_for_time_with_periodic_events(window, params, df_mood, start_time, display_time_img, keyboard, prefix, 0)
            # helpers.wait_for_time(window, params, start_time, display_time_img, keyboard, df_mood)

            display_time_img_angry = 2
            if len(temp_naturals) == 3:
                helpers.show_image_with_scream(
                    window=window,
                    image_path=f"./img/Angry/{angry_img_name}.jpg",
                    sound_path="./sound/shock_sound_1.mp3",
                    duration=display_time_img_angry,
                    keyboard=keyboard,
                    escape_callback=lambda: helpers.graceful_shutdown(window, params, df_mood),
                    size=(1.5, 1.5),
                    volume=0.4
                )
                helpers.add_event(params, f'{prefix}_angry')

            # ITI
            display_time_iti = params["blockDuration"] - display_time_img - display_time_img_angry # - display_time_plus
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