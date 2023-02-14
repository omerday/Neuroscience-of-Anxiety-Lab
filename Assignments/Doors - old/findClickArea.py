# tmp
# # Green: (185,160),(130,160),(185,-210),(130,-210)
# # Red: (-185, 160),(-130,160),(-185,-210),(-130,-210)

import sys
sys.path.insert(1, 'src')

from psychopy import visual, event,core
import time

# Import developer-defined functions
import sys
sys.path.insert(1, 'src')
import datetime
import pandas as pd
from psychopy import visual,core,event

import time

# Initialization
# Declare primary task parameters.
params = {
    'screenSize' : (1024,780),
}

## Setup Psychopy Window.
win = visual.Window((1024,780), monitor="testMonitor",color="black",winType='pyglet')


img = visual.ImageStim(win=win, image="./img/aoi.jpg", units="pix", opacity=1,
                       size=(params['screenSize'][0], params['screenSize'][1]))

circle = visual.Circle(win=win, units="pix", fillColor='black', lineColor='white', edges=1000,
                       pos=(110,-320),
                       radius=5)

img.draw()
circle.draw()
win.flip()

c = event.getKeys()

# Green: (-350,-320), (-350,290), (-110,290), (-110,-320)
# Red: (350,-320), (350,290), (110,290),(110,-320)
