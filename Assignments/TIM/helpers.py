import time
from psychopy import visual, core
from psychopy.iohub.client.keyboard import Keyboard
import random
import VAS


""" 
We need to add a method that presents a cross screen for a period of 4-6 seconds.
The cross image is located under the ./img folder
keep the min and max times as arguments in params.
The method will be called here to create a little wait before the presentation of the first square.
"""
def pre_ITI(window:visual.Window, params: dict, keyboard:Keyboard):
    display_time = random.uniform(params['preITIMin'], params['preITIMax'])
    square = visual.ImageStim(window, image=f"./img/plus.jpeg", units="norm", size=(2, 2))
    square.draw()
    window.flip()
    start_time = time.time()
    wait_for_time(window, start_time, display_time, keyboard)


"""        
We need to add a method that presents a blank screen for a period of 7-9 seconds.
The cross image is located under the ./img folder
keep the min and max times as arguments in params.
The method will be called here to create a little wait after the heat rating
"""
def post_ITI(window:visual.Window, params: dict, keyboard):
    display_time = random.uniform(params['postITIMin'], params['postITIMax'])
    square = visual.ImageStim(window, image=f"./img/blank.jpeg", units="norm", size=(2, 2))
    square.draw()
    window.flip()
    start_time = time.time()
    wait_for_time(window, start_time, display_time, keyboard)


"""
In the second paradigm, only a one, medium-sized square is presented on the screen for a randomized
time of 10-14, following a heat pain.
So we need to add an argument in the opening screen to determine whether we want multiple squares or one,
and modify this section accordingly with an "if" statement.
(Maybe dividing to two functions would be prettier?)
"""
def second_paradigm(window: visual.Window, params: dict, device, io):
    display_time = random.uniform(params['secondParadigmMin'], params['secondParadigmMax'])


def wait_for_time(window: visual.Window, start_time, display_time, keyboard):
    while time.time() < start_time + display_time:
        for event in keyboard.getKeys():
            if event.key == "escape":
                # TODO: Add Cooldown function
                window.close()
                core.quit()
        core.wait(0.05)