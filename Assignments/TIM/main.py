import os
import time
import pandas as pd
from psychopy.iohub import launchHubServer
from psychopy import visual, core, event, monitors
import configDialog
import squareRun
import instructions
import json
import serial
from VAS import *
from serialHandler import *

io = launchHubServer()

debug = False
configDialogBank = configDialog.get_user_input(debug)

params = {
    "subject": configDialogBank[0],
    "session": configDialogBank[1],
    "gender": configDialogBank[2],
    "language": configDialogBank[3],
    "fmriVersion": configDialogBank[4],
    'temps': [configDialogBank[5], configDialogBank[6], configDialogBank[7]],
    'Ts': ['T2', 'T4', 'T8'],
    # "T2": configDialogBank[5],
    # "T4": configDialogBank[6],
    # "T6": configDialogBank[7],
    # "T8": configDialogBank[8],
    "paradigm": configDialogBank[8],
    "painSupport": configDialogBank[9],
    "recordPhysio": configDialogBank[10],
    "skipInstructions": configDialogBank[11],
    "continuousShape": configDialogBank[12],
    "fullScreen": True,
    "screenSize": (1024, 768),
    "startTime": time.time(),
    'port': 'COM4',
    'nTrials': 6,  # number of squares in each block
    'nBlocks': 6,  # number of blocks (aka runs) - need time to move electrode in between
    'painDur': 4,  # time of heat sensation (in seconds)
    'painRateDuration': 7.0,
    'squareDurationMin': 4,  # minimum duration for each square
    'squareDurationMax': 7,  # maximum duration for each square
    'colors': ['Green', 'Yellow', 'Red'],
    'preITIMin': 4,
    'preITIMax': 6,
    'postITIMin': 7,
    'postITIMax': 9,
    'secondParadigmMin': 10,
    'secondParadigmMax': 14,
    'continuousPresentTimeMin': 2,
    'continuousPresentTimeMax': 2.5,

}

if not os.path.exists("./data"):
    os.mkdir("data")
with open("./data/TIMconfig.json", 'w') as file:
    json.dump(params, file, indent=3)

# TODO: Create a dataframe and support saving data (@yuval) for the end
# Take a look at the data handler and it's usage in the NPU!
params['serialBiopac'] = serial.Serial(params['port'], 115200, bytesize=serial.EIGHTBITS, timeout=1) if params['recordPhysio'] else None

if params['recordPhysio']:
    report_event(params['serialBiopac'], 255)

device = None
if params['painSupport']:
    import heatHandler
    device = heatHandler.initiate_medoc_device()

io = launchHubServer()

window = visual.Window(monitor="testMonitor", fullscr=params['fullScreen'], color=(217, 217, 217))
window.flip()

core.wait(0.5)

# TODO: Display a Welcome Message (@yuval)
# We need to create a slide on powerpoint and export it as a JPEG
if params['language'] == 'English':
    name_prefix_1 = "Welcome_E"
    name_prefix_2 = "finish_E"
elif params['gender'] == 'Female':
    name_prefix_1 = "Welcome_F"
    name_prefix_2 = "finish_F"
else:
    name_prefix_1 = "Welcome_M"

image = visual.ImageStim(window, image=f"./img/instructions/{name_prefix_1}.jpeg", units="norm", size=(2, 2))
image.draw()

window.flip()

# First mood VAS
run_vas(window, io, params, 'mood')
if params['recordPhysio']:
    report_event(params['serialBiopac'], BIOPAC_EVENTS['PreVas_rating'])

if not params['skipInstructions']:
    instructions.instructions(window, params, io)

for i in range(params['nBlocks']):
    # Middle Mood VAS
    if i == params['nBlocks']/2:
        run_vas(window, io, params, 'mood')
        if params['recordPhysio']:
            report_event(params['serialBiopac'], BIOPAC_EVENTS['MidRun_rating'])
    squareRun.square_run(window, params, device, io)

# Final Mood VAS
run_vas(window, io, params, 'mood')
if params['recordPhysio']:
    report_event(params['serialBiopac'], BIOPAC_EVENTS['PostRun_rating'])

# TODO: Implement the main code (@yuval)
"""
What we need to do is implement the routine of the code.
For nBlocks, we need to run the square_run function, and then run a mood VAS.
we also need to add a function that, for the first n-1 blocks, after the end of the VAS will show a
slide saying "Let's rest a little. Please wait for the instructor" or something like that, and wait for a spacebar
keypress.
"""