import random
import time

import pandas as pd
from psychopy import visual, core, sound
import helpers

CONDITIONING_FLOW = [{"image": "CS-", "scream": False},
                     {"image": "CS+", "scream": False},
                     {"image": "CS-", "scream": False},
                     {"image": "CS+", "scream": True},
                     {"image": "CS-", "scream": False},
                     {"image": "CS+", "scream": False},]

ANGRY_IMAGE_ONSET_TIME = 2

def condition_long_version(params, window: visual.Window, io, keyboard, df_mood: pd.DataFrame):
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
            if len(temp_naturals) == 4:
                helpers.add_event(params, f'{prefix}_angry')
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


def condition_short_version(params, window: visual.Window, io, keyboard, df_mood: pd.DataFrame):
    for i, trial in enumerate(CONDITIONING_FLOW):
        image_type = trial['image']
        scream = trial['scream']

        prefix_for_events = f"N{params['faceCombination'][image_type]}"
        neut_image = f"N{params['faceCombination'][image_type]}_F.jpg"
        # displaying the img
        display_time_img = random.uniform(params['faceDurationMin'], params['faceDurationMax'])
        img = visual.ImageStim(window, image=f"./img/Natural/{neut_image}.jpg", units="norm", size=(1.5, 1.5))
        img.draw()
        window.mouseVisible = False
        window.flip()
        start_time = time.time()
        # add event every 2 sec
        helpers.wait_for_time_with_periodic_events(window, params, df_mood, start_time, display_time_img, keyboard,
                                                   prefix_for_events, 0)

        if scream:
            angry_image = f"A{params['faceCombination'][image_type]}_F.jpg"
            helpers.add_event(params, f'{prefix_for_events}_angry')
            helpers.show_image_with_scream(
                window=window,
                image_path=f"./img/Angry/{angry_image}.jpg",
                sound_path="./sound/shock_sound_1.mp3",
                duration=ANGRY_IMAGE_ONSET_TIME,
                keyboard=keyboard,
                escape_callback=lambda: helpers.graceful_shutdown(window, params, df_mood),
                size=(1.5, 1.5),
                volume=0.4
            )

        # ITI
        display_time_iti = params["blockDuration"] - display_time_img - ANGRY_IMAGE_ONSET_TIME
        blank = visual.ImageStim(window, image=f"./img/blank.jpeg", units="norm", size=(2, 2))
        blank.draw()
        window.mouseVisible = False
        window.flip()
        start_time = time.time()
        # adding event when starting ITI
        helpers.add_event(params, f'{prefix_for_events}_ITIpre')
        helpers.wait_for_time(window, params, df_mood, start_time, display_time_iti, keyboard)
        # adding event after ITI
        helpers.add_event(params, f'{prefix_for_events}_ITIpost')