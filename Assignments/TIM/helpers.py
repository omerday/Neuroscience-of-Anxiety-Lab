import time
from psychopy import visual, core
from psychopy.iohub.client.keyboard import Keyboard
import random
import serial, serialHandler
import VAS


def iti(window:visual.Window, params: dict, iti_type, keyboard):
    display_time = random.uniform(params[f'{iti_type}ITIMin'], params[f'{iti_type}ITIMax'])
    image = "./img/blank.jpeg" if iti_type == "post" else "./img/plus.jpeg"
    square = visual.ImageStim(window, image=image, units="norm", size=(2, 2))
    square.draw()
    window.flip()
    start_time = time.time()
    wait_for_time(window, start_time, display_time, keyboard)

# image = "blank.jpg" if type == "post" else "cross.jpg"

def wait_for_time(window: visual.Window, start_time, display_time, keyboard):
    while time.time() < start_time + display_time:
        for event in keyboard.getKeys():
            if event.key == "escape":
                # TODO: Add Cooldown function
                window.close()
                core.quit()
        core.wait(0.05)


def wait_for_space(window: visual.Window, io):
    keyboard = io.devices.keyboard
    while True:
        for event in keyboard.getKeys():
            if event.key == "space":
                return
            elif event.key == "escape":
                # TODO: Add Cooldown function
                window.close()
                core.quit()
        core.wait(0.05)

def graceful_shutdown()