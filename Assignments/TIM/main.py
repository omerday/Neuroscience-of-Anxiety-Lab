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

device = None
if params['painSupport']:
    import heatHandler
    device = heatHandler.initiate_medoc_device()

io = launchHubServer()

window = visual.Window(monitor="testMonitor", fullscr=True, color=(217, 217, 217))
window.flip()

core.wait(0.5)

#TODO: Add mood VAS

if not params['skipInstructions']:
    instructions.instructions(window, params, io)

squareRun.square_run(window, params, device, io)
