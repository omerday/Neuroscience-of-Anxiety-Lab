import time
from psychopy import visual, core
from psychopy.iohub.client.keyboard import Keyboard
import random
import VAS
from helpers import pre_ITI, post_ITI, wait_for_time


def square_run(window: visual.Window, params: dict, device, io):
    keyboard = io.devices.keyboard
    repeats = params['nTrials'] // len(params['colors'])
    colors_order = []
    for color in params['colors']:
        for i in range(repeats):
            colors_order.append(color)
    while colors_order:
        pre_ITI(window, params, keyboard)
        curr_color = random.choice(colors_order)
        colors_order.remove(curr_color)
        color_index = params['colors'].index(curr_color)
        temperature = params['temps'][color_index]
        # TODO: Add 2nd paradigm
        """
        In the second paradigm, only a one, medium-sized square is presented on the screen for a randomized
        time of 10-14, following a heat pain.
        So we need to add an argument in the opening screen to determine whether we want multiple squares or one,
        and modify this section accordingly with an "if" statement.
        (Maybe dividing to two functions would be prettier?)
        """
        if params['secondParadigm']:
            display_time = random.uniform(params['secondParadigmMin'], params['secondParadigmMax'])
            square = visual.ImageStim(window, image=f"./img/squares/{curr_color}_{3}.jpeg", units="norm", size=(2,2))
            square.draw()
            square.flip()
            start_time = time.time()
            wait_for_time(window, start_time, display_time, keyboard)

        if params['firstParadigm']:
            for i in range(1, 6):
                display_time = random.uniform(params['squareDurationMin'], params['squareDurationMax'])
                square = visual.ImageStim(window, image=f"./img/squares/{curr_color}_{i}.jpeg", units="norm", size=(2,2))
                square.draw()
                window.flip()
                start_time = time.time()
                if params['continuousShape'] or i == 5:
                    wait_for_time(window, start_time, display_time, keyboard)
                else:
                    # TODO: Add randomization period to the params
                    present_time = random.uniform(2,2.5)
                    wait_for_time(window, start_time, present_time, keyboard)
                    square.image = "./img/squares/blank.jpg"
                    square.draw()
                    window.flip()
                    wait_for_time(window, start_time, display_time, keyboard)

        if params['painSupport']:
            import heatHandler
            heatHandler.deliver_pain(window, float(temperature), device)

        VAS.run_vas(window, io, params, "PainRating", params['painRateDuration'])

        post_ITI(window, params, keyboard)



