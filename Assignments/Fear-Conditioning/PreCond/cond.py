import random
import time

from psychopy import visual
import helpers


def pre_cond(params, window: visual.Window, io, keyboard):
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
            temp_naturals.remove(curr_img)
            display_time_img_angry = 0

            # displaying the plus image before the shape
            display_time_plus = random.uniform(params['plusDurationMin'], params['plusDurationMax'])
            plus = visual.ImageStim(window, image=f"./img/plus.jpeg", units="norm", size=(2, 2))
            plus.draw()
            window.mouseVisible = False
            window.flip()
            start_time = time.time()
            helpers.wait_for_time(window, params, start_time, display_time_plus, keyboard)

            # displaying the img
            display_time_img = random.uniform(params['faceDurationMin'], params['faceDurationMax'])
            img = visual.ImageStim(window, image=f"./img/natural/{img_name}.jpeg", units="norm", size=(2, 2))
            img.draw()
            window.mouseVisible = False
            window.flip()
            start_time = time.time()
            helpers.wait_for_time(window, params, start_time, display_time_img, keyboard)

            if len(temp_naturals) == 4:
                display_time_img_angry = 2
                angry_img = visual.ImageStim(window, image=f"./img/Angry/{angry_img_name}.jpeg", units="norm", size=(2, 2))
                angry_img.draw()
                # TODO: צעקה
                window.mouseVisible = False
                window.flip()
                start_time = time.time()
                helpers.wait_for_time(window, params, start_time, display_time_img_angry, keyboard)

            # ITI
            display_time_iti = params["blockDuration"] - display_time_img - display_time_plus - display_time_img_angry
            blank = visual.ImageStim(window, image=f"./img/blank.jpeg", units="norm", size=(2, 2))
            blank.draw()
            window.mouseVisible = False
            window.flip()
            start_time = time.time()
            helpers.wait_for_time(window, params, start_time, display_time_iti, keyboard)