from psychopy import visual, core, event
from psychopy.iohub import launchHubServer
from psychopy.iohub.client.keyboard import Keyboard
from psychopy.visual import ratingscale
from psychopy import sound
import psychtoolbox as ptb


def wait_for_space(window: visual.Window, io):
    keyboard = io.devices.keyboard
    while True:
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == " ":
                return
            if event.key == "escape":
                window.close()
                core.quit()


def wait_for_space_with_replay(window, io):
    keyboard = io.devices.keyboard
    while True:
        keys = keyboard.getPresses()
        for event in keys:
            if event.key == 'r' or event.key == 'R':
                return True
            elif event.key == ' ':
                return False
            elif event.key == "escape":
                window.close()
                core.quit()


def wait_for_space_with_rating_scale(window, img: visual.ImageStim, io, params:dict):
    keyboard = io.devices.keyboard
    print(-params["screenSize"][1]/2 + 100)
    scale = ratingscale.RatingScale(win=window, scale=None,labels=["0", "10"], low=0, high=10, markerStart=5, showAccept=False, markerColor="Red",
                                   acceptKeys=["space"], textColor="Black", lineColor="Black", pos=(0,-window.size[1]/2 + 200))
    while scale.noResponse:
        img.draw()
        scale.draw()
        window.flip()


def play_startle_and_wait(window: visual.Window, io):
    soundToPlay = sound.Sound("./sounds/startle_probe.wav")
    core.wait(2)
    now = ptb.GetSecs()
    soundToPlay.play(when=now)
    core.wait(1)
    keyboard = io.devices.keyboard
    while True:
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == " ":
                soundToPlay.stop()
                return
            if event.key == "escape":
                window.close()
                core.quit()
