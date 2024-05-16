import time
from psychopy import visual, core
from psychopy.iohub.client.keyboard import Keyboard
import random
import VAS
import helpers


def square_run(window: visual.Window, params: dict, device, io):
    keyboard = io.devices.keyboard
    repeats = params['nTrials'] // len(params['colors'])
    colors_order = []
    for color in params['colors']:
        for i in range(repeats):
            colors_order.append(color)
    while colors_order:
        helpers.iti(window, params, 'pre', keyboard)
        curr_color = random.choice(colors_order)
        colors_order.remove(curr_color)
        color_index = params['colors'].index(curr_color)
        temperature = params['temps'][color_index]

        if params['paradigm'] == 1:
            for i in range(1, 6):
                display_time = random.uniform(params['squareDurationMin'], params['squareDurationMax'])
                square = visual.ImageStim(window, image=f"./img/squares/{curr_color}_{i}.jpeg", units="norm", size=(2,2))
                square.draw()
                window.flip()
                start_time = time.time()
                if params['continuousShape'] or i == 5:
                    helpers.wait_for_time(window, start_time, display_time, keyboard)
                else:
                    # TODO: Add randomization period to the params
                    present_time = random.uniform(2,2.5)
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
            heatHandler.deliver_pain(window, float(temperature), device)

        VAS.run_vas(window, io, params, "PainRating", params['painRateDuration'])

        helpers.iti(window, params, 'post', keyboard)



