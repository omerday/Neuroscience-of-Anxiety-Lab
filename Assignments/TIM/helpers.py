import time
from psychopy import visual, core
from psychopy.iohub.client.keyboard import Keyboard
import random
import VAS


"""        
We need to add a method that presents a blank screen for a period of 7-9 seconds.
The cross image is located under the ./img folder
keep the min and max times as arguments in params.
The method will be called here to create a little wait after the heat rating
"""
def iti(window:visual.Window, params: dict, iti_type, keyboard):
    display_time = random.uniform(params[f'{iti_type}ITIMin'], params[f'{iti_type}ITIMax'])
    image = "./img/blank.jpeg" if iti_type == "post" else "./img/plus.jpeg"
    square = visual.ImageStim(window, image=image, units="norm", size=(2, 2))
    square.draw()
    window.flip()
    start_time = time.time()
    wait_for_time(window, start_time, display_time, keyboard)

# image = "blank.jpg" if type == "post" else "cross.jpg"
"""
In the second paradigm, only a one, medium-sized square is presented on the screen for a randomized
time of 10-14, following a heat pain.
So we need to add an argument in the opening screen to determine whether we want multiple squares or one,
and modify this section accordingly with an "if" statement.
(Maybe dividing to two functions would be prettier?)
"""

def wait_for_time(window: visual.Window, start_time, display_time, keyboard):
    while time.time() < start_time + display_time:
        for event in keyboard.getKeys():
            if event.key == "escape":
                # TODO: Add Cooldown function
                window.close()
                core.quit()
        core.wait(0.05)