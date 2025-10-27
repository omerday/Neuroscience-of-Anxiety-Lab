import random
import time

import pandas as pd
from psychopy import visual

import helpers


def test_long_version(params, window: visual.Window, io, keyboard, df_mood: pd.DataFrame):
    for i in range(3):
        temp_naturals = []
        for N in params['natural']:
            temp_naturals.append(N)

        prev_gender = ""
        counter = 1
        while temp_naturals:
            # choosing natural face
            neut_img_name = random.choice(temp_naturals)
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
                prefix = neut_img_name.split('_')[0]  # for the events
                temp_naturals.remove(neut_img_name)

            # displaying the natural face
            display_time_n = random.uniform(params['faceDurationMin'], params['faceDurationMax'])
            shape = visual.ImageStim(window, image=f"./img/long/Natural/{neut_img_name}.jpeg", units="norm", size=(1.5, 2))
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
            helpers.add_event(params, f'{prefix}_ITIstart')
            helpers.wait_for_time(window, params, df_mood, start_time, display_time_iti, keyboard)
            # adding event after ITI
            helpers.add_event(params, f'{prefix}_ITIend')


def test_short_version(params, window: visual.Window, io, keyboard, df_mood: pd.DataFrame):
    sequence = helpers.generate_test_sequence(params['testRepetitions'])
    for trial in sequence:
        stim_face_number = params['faceCombination'][trial]
        image_name = f"{stim_face_number}_N"
        prefix = trial

        # displaying the natural face
        display_time_n = params['faceDurationTest']
        shape = visual.ImageStim(window, image=f"./img/short/Natural/{image_name}.jpeg", units="norm", size=(2, 2))
        shape.draw()
        window.mouseVisible = False
        window.flip()
        start_time = time.time()

        # adding event every 2 sec
        helpers.wait_for_time_with_periodic_events(window, params, df_mood, start_time, display_time_n, keyboard,
                                                   prefix, 0)

        # ITI
        display_time_iti = random.uniform(params['ITIDurationTestMin'], params['ITIDurationTestMax'])
        blank = visual.ImageStim(window, image=f"./img/blank.jpeg", units="norm", size=(2, 2))
        blank.draw()
        window.mouseVisible = False
        window.flip()
        start_time = time.time()
        # adding event when starting ITI
        helpers.add_event(params, f'{prefix}_ITIstart')
        helpers.wait_for_time(window, params, df_mood, start_time, display_time_iti, keyboard)
        # adding event after ITI
        helpers.add_event(params, f'{prefix}_ITIend')