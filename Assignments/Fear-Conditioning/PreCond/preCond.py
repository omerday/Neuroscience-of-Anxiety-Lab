import time
import helpers
from psychopy import visual
import random
from psychopy.iohub.client.keyboard import Keyboard

def pre_cond(params, window: visual.Window, io, keyboard, mood_df):
    temp_shapes = []
    for shape in params['shapes']:
        temp_shapes.append(shape)

    while temp_shapes:
        # choosing shape
        curr_shape = random.choice(temp_shapes)
        temp_shapes.remove(curr_shape)
        shape_name = params['shapes'].index(curr_shape)

        """
        # displaying the plus image before the shape
        display_time_plus = random.uniform(params['plusDurationMin'], params['plusDurationMax'])
        plus = visual.ImageStim(window, image=f"./img/plus.jpeg", units="norm", size=(2, 2))
        plus.draw()
        window.mouseVisible = False
        window.flip()
        start_time = time.time()
        # plus add event
        helpers.add_event(params, f'S_plus')
        helpers.wait_for_time(window, params, mood_df, start_time, display_time_plus, keyboard)
        """

        # displaying the shape
        display_time_shape = random.uniform(params['shapeDurationMin'], params['shapeDurationMax'])
        shape = visual.ImageStim(window, image=f"./img/shapes/{curr_shape}.jpeg", units="norm", size=(2, 2))
        shape.draw()
        window.mouseVisible = False
        window.flip()
        start_time = time.time()
        # add event every 2 sec
        helpers.wait_for_time_with_periodic_events(window, params, mood_df, start_time, display_time_shape, keyboard,
                                                   'S', 0)

        # ITI
        display_time_iti = params["blockDuration"] - display_time_shape # - display_time_plus
        blank = visual.ImageStim(window, image=f"./img/blank.jpeg", units="norm", size=(2, 2))
        blank.draw()
        window.mouseVisible = False
        window.flip()
        start_time = time.time()
        # adding event when starting ITI
        helpers.add_event(params, f'S_ITIpre')
        helpers.wait_for_time(window, params, mood_df, start_time, display_time_iti, keyboard)
        # adding event after ITI
        helpers.add_event(params, f'S_ITIpost')