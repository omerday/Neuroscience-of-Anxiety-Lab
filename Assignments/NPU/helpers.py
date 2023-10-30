from psychopy import visual, core, event
from psychopy.iohub import launchHubServer
from psychopy.iohub.client.keyboard import Keyboard


def wait_for_space(window: visual.Window, io):
    keyboard = io.devices.keyboard
    while True:
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == " ":
                return
            if event.key == "escape":
                window.close()
                core.quit()