import os
import time
import pandas as pd
from psychopy.iohub import launchHubServer
from psychopy import visual, core, event, monitors
import configDialog
import squareRun
import instructions
import json
from VAS import *
from serialHandler import *
from helpers import *
from dataHandler import *
import logging
from datetime import datetime

io = launchHubServer()

debug = False
configDialogBank = configDialog.get_user_input(debug)

params = {
    "subject": configDialogBank[0],
    "session": configDialogBank[1],
    "gender": configDialogBank[2],
    "language": configDialogBank[3],
    "fmriVersion": configDialogBank[4],
    'nTrials': 6,  # number of squares in each block
    'nBlocks': configDialogBank[5],  # number of blocks (aka runs) - need time to move electrode in between
    'temps': [configDialogBank[6], configDialogBank[7], configDialogBank[8]],
    'Ts': ['T2', 'T4', 'T8'],
    # "T2": configDialogBank[5],
    # "T4": configDialogBank[6],
    # "T6": configDialogBank[7],
    # "T8": configDialogBank[8],
    "painSupport": configDialogBank[9],
    "recordPhysio": configDialogBank[10],
    "skipInstructions": configDialogBank[11],
    "continuousShape": configDialogBank[12],
    "fullScreen": True,  # True,
    "screenSize": (1024, 768),
    "startTime": time.time(),
    'port': 'COM4',
    'painDur': 4,  # time of heat sensation (in seconds)
    'painRateDuration': 7.0,
    'squareDurationMin': 4,  # minimum duration for each square
    'squareDurationMax': 7,  # maximum duration for each square
    'colors': ['Green', 'Yellow', 'Red'],
    'fixationBeforeBlock': 8,
    'preITIMin': 3,
    'preITIMax': 5,
    'postITIMin': 7,
    'postITIMax': 9,
    'secondParadigmSquareOnset': 2,
    'secondParadigmSquareBlankScreen': 8,
    'secondParadigmJitterMin': 0,
    'secondParadigmJitterMax': 1,
    'preRatingITI': 2,
    'secondParadigmMin': 8,
    'secondParadigmMax': 10,
    'continuousPresentTimeMin': 2,
    'continuousPresentTimeMax': 2.5,
    'dontSleepAfterTemp': configDialogBank[13],
    'tempRampUpTime': 750 if configDialogBank[14] else 300,
    'fmriStartTime': 0,
}

if not os.path.exists("./data"):
    os.mkdir("data")
with open("./data/TIMconfig.json", 'w') as file:
    json.dump(params, file, indent=3)

print(f"===========================================\nStarting Run for Subject {params['subject']}\n===========================================")

df_pain, df_mood = setup_data_frame()
params['serialBiopac'] = serial.Serial(params['port'], 115200, bytesize=serial.EIGHTBITS, timeout=1) if params[
    'recordPhysio'] else None


if params['recordPhysio']:
    report_event(params['serialBiopac'], 255)

device = None
if params['painSupport']:
    import heatHandler
    device = heatHandler.initiate_medoc_device()

window = visual.Window(monitor="testMonitor", fullscr=params['fullScreen'], color=(210, 210, 210))
window.mouseVisible = False
window.flip()

core.wait(0.5)

image = visual.ImageStim(window,
                         image=f"./img/instructions/Welcome_{'E' if params['language'] == 'English' else params['gender'][0]}.jpeg",
                         units="norm", size=(2, 2))
image.draw()
window.mouseVisible = False
window.flip()
wait_for_space(window, params, device, df_mood, df_pain, io)

if params["fmriVersion"]:
    # T1 Sequence
    helpers.performT1Scan(window, params, io)
    # Button Practice
    _ = run_vas(window, io, params, 'mood', mood_df=df_mood, pain_df=df_pain, device=device, practice=True)

# First mood VAS
if params['recordPhysio']:
    report_event(params['serialBiopac'], BIOPAC_EVENTS['PreVas_rating'])
scores = run_vas(window, io, params, 'mood', mood_df=df_mood, pain_df=df_pain, device=device)
df_mood = insert_data_mood("pre", scores, df_mood)

if not params['skipInstructions']:
    instructions.instructions(window, params, io)

for i in range(1, params['nBlocks'] + 1):
    df_pain = squareRun.square_run(window, params, device, io, df_pain, df_mood, i)
    # Middle Mood VAS
    if i == params['nBlocks'] // 2:
        if params['recordPhysio']:
            report_event(params['serialBiopac'], BIOPAC_EVENTS['MidRun_rating'])
        scores = run_vas(window, io, params, 'mood', mood_df=df_mood, pain_df=df_pain, device=device)
        df_mood = insert_data_mood("mid", scores, df_mood)
    if not params['fmriVersion']:
        helpers.wait_for_RA(window, params, device, df_mood, df_pain, io)

# Final Mood VAS
if params['recordPhysio']:
    report_event(params['serialBiopac'], BIOPAC_EVENTS['PostRun_rating'])
scores = run_vas(window, io, params, 'mood', mood_df=df_mood, pain_df=df_pain, device=device)
df_mood = insert_data_mood("post", scores, df_mood)

image = visual.ImageStim(window,
                         image=f"./img/instructions/finish_{'E' if params['language'] == 'English' else params['gender'][0]}.jpeg",
                         units="norm", size=(2, 2))
image.draw()
window.mouseVisible = False
window.flip()

wait_for_space(window, params, device, df_mood, df_pain, io)
graceful_shutdown(window, params, device, df_mood, df_pain)
