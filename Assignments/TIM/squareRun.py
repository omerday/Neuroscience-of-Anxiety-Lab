import time
from psychopy import visual, core
from psychopy.iohub.client.keyboard import Keyboard
import random
import VAS


def square_run(window: visual.Window, params: dict, device, io):
    keyboard = io.devices.keyboard
    # TODO: Add pre-ITI
    """
    We need to add a method that presents a cross screen for a period of 4-6 seconds.
    The cross image is located under the ./img folder
    keep the min and max times as arguments in params.
    The method will be called here to create a little wait before the presentation of the first square.
    """
    repeats = params['nTrials'] // len(params['colors'])
    colors_order = []
    for color in params['colors']:
        for i in range(repeats):
            colors_order.append(color)
    while colors_order:
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

        # TODO: Add Post ITI
        """
        We need to add a method that presents a blank screen for a period of 7-9 seconds.
        The cross image is located under the ./img folder
        keep the min and max times as arguments in params.
        The method will be called here to create a little wait after the heat rating
        """


def wait_for_time(window:visual.Window, start_time, display_time, keyboard):
    while time.time() < start_time + display_time:
        for event in keyboard.getKeys():
            if event.key == "escape":
                # TODO: Add Cooldown function
                window.close()
                core.quit()
        core.wait(0.05)
