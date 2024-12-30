from psychopy import visual, core
import time
from psychopy.iohub.client.keyboard import Keyboard

def graceful_shutdown(window, params):
    print(f"Experiment Ended\n===========================================")
    window.close()
    core.quit()
    exit()

def wait_for_time(window: visual.Window, params, start_time, display_time, keyboard):
    while time.time() < start_time + display_time:
        for event in keyboard.getKeys():
            if event.key == "escape":
                graceful_shutdown(window, params)
        core.wait(0.05)