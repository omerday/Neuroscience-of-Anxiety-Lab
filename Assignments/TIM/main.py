import os
import time
import pandas as pd
from psychopy.iohub import launchHubServer
from psychopy import visual, core, event, monitors
import configDialog
import squareRun
import instructions
import json

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

}

if not os.path.exists("./data"):
    os.mkdir("data")
with open("./data/TIMconfig.json", 'w') as file:
    json.dump(params, file, indent=3)

# TODO: Create a dataframe and support saving data (@yuval)
# Take a look at the data handler and it's usage in the NPU!

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

# TODO: Add initial mood VAS (@yuval)

if not params['skipInstructions']:
    instructions.instructions(window, params, io)

squareRun.square_run(window, params, device, io)

# TODO: Implement the main code (@yuval)
"""
What we need to do is implement the routine of the code.
For nBlocks, we need to run the square_run function, and then run a mood VAS.
we also need to add a function that, for the first n-1 blocks, after the end of the VAS will show a
slide saying "Let's rest a little. Please wait for the instructor" or something like that, and wait for a spacebar
keypress.
"""