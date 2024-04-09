import os
import time
import pandas as pd
from psychopy.iohub import launchHubServer
from psychopy import visual, core, event, monitors
import configDialog

io = launchHubServer()

debug = False
configDialogBank = configDialog.get_user_input(debug)

params = {
    "subject": configDialogBank[0],
    "session": configDialogBank[1],
    "gender": configDialogBank[2],
    "language": configDialogBank[3],
    "fmriVersion": configDialogBank[4],
    "T2": configDialogBank[5],
    "T4": configDialogBank[6],
    "T6": configDialogBank[7],
    # "T8": configDialogBank[8],
    "painSupport": configDialogBank[9],
    "recordPhysio": configDialogBank[10],
    "skipInstructions": configDialogBank[11],
    "continuousShape": configDialogBank[12],
    "fullScreen": configDialogBank[13] if debug is True else True,
    "saveDataAtQuit": configDialogBank[14] if debug is True else True,
    "saveConfig": configDialogBank[15] if debug is True else True,
    "screenSize": (1024, 768),
    "startTime": time.time(),
    'port': 'COM4',
    'nTrials': 6,  # number of squares in each block
    'nBlocks': 6,  # number of blocks (aka runs) - need time to move electrode in between
    'painDur': 4,  # time of heat sensation (in seconds)
    'painRateDuration': 7.0,
    'squareDurationMin': 3,  # minimum duration for each square
    'squareDurationMax': 6,  # maximum duration for each square
    'colors': ['Green', 'Yellow', 'Red'],
}