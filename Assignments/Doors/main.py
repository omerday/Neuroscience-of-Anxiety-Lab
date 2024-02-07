import time
import json
import pandas
from psychopy import visual, core, event
import DoorPlay
import helpers
from psychopy.iohub import launchHubServer
import runConfigDialog
import dataHandler
import serialHandler
import DoorPlayInfra
from instructionsScreen import show_instructions
import VAS
import serial
import os

io = launchHubServer()

# log = LoggerSetup.set_up_logger()
debug = False
configDialogBank = runConfigDialog.user_input_play(debug)

params = {
    'Subject': configDialogBank[0],
    'Session': configDialogBank[1],
    'practiceTrials': configDialogBank[2],  # Number if Practice Trials, taken from Config Dialog
    'numOfDoors': configDialogBank[3],  # Number of Screens in the 1st task, either 49 (7*7) or 36 (6*6)
    'numOfSimulationDoors': 5,
    'numOfTasks': configDialogBank[4],
    'startingDistance': configDialogBank[5],  # Decide whether the starting distance is random, or fixed on 50
    'recordPhysio': configDialogBank[6],
    'sensitivity': configDialogBank[7],
    'doorLayout': configDialogBank[8],
    'ITIDurationMin': 1,
    'ITIDurationMax': 2.5,
    'keyboardMode': configDialogBank[9],
    'screenSize': (1024, 768),  # Get Screen Resolution to match Full Screen
    'soundOn': configDialogBank[10],
    'beeps': False,
    'outcomeString': True,   # True if we want to print the outcome amount, otherwise it will just show a monster / a fairy
    'skipInstructions': configDialogBank[11],
    'language': configDialogBank[12],
    'reducedEvents': False,
    'fullScreen': configDialogBank[13] if debug else True,
    'saveDataAtQuit': configDialogBank[14] if debug else True,
    'startTime': time.time(),
    'saveAsDefault': configDialogBank[15] if debug else True,
    'doorImagePathPrefix': './img/doors1/' if configDialogBank[8] == "P - R" else './img/doors2/',
    'doorOutcomePath': './img/outcomes/',
    'imageSuffix': '.jpg',
    'port': 'COM4',
}

if params['saveAsDefault']:
    if not os.path.exists("./data"):
        os.mkdir("data")
    with open("./data/doorsConfig.json", 'w') as file:
        json.dump(params, file, indent=3)

# Initialize serial port
ser = serial.Serial(params['port'], 115200, bytesize=serial.EIGHTBITS, timeout=1) if params['recordPhysio'] else None
if params['recordPhysio']:
    serialHandler.report_event(ser, 255)

# Initialize DataFrame
params, Df, mini_df, summary_df = dataHandler.setup_data_frame(params)

# Initialize Screen
window = visual.Window(params['screenSize'], monitor="testMonitor", color="black", winType='pyglet',
                       fullscr=True if params['fullScreen'] else False, units="pix")
image = visual.ImageStim(win=window, image="./img/ITI_fixation.jpg", units="norm", opacity=1,
                         size=(2, 2) if not params['fullScreen'] else None)
image.draw()
window.mouseVisible = False
window.update()
if params['keyboardMode']:
    helpers.wait_for_space_no_df(window, io)
else:
    helpers.wait_for_joystick_no_df(window)

# Run VAS
Df, mini_df, summary_df = VAS.beginning_vas(window, params, Df, mini_df, summary_df, io)

if not params['skipInstructions']:

    # Show Instructions
    Df, mini_df = show_instructions(window, params, image, Df, mini_df, io)

    # Practice run
    Df, mini_df, summary_df = DoorPlay.practice_run(window, params, Df, mini_df, summary_df, io, ser)

    # Simulation run
    Df, mini_df, summary_df, totalCoins = DoorPlay.run_task(window, params, 0, 0, Df, mini_df, summary_df, io, ser)

# Task 1
Df, mini_df, summary_df, totalCoins = DoorPlay.run_task(window, params, 1, 0, Df, mini_df, summary_df, io, ser)

roundNum = 2
while roundNum <= params['numOfTasks']:
    # Mid-VAS
    Df, mini_df, summary_df = VAS.middle_vas(window, params, Df, mini_df, summary_df, roundNum, io)

    # Task 2
    Df, mini_df, summary_df, totalCoins = DoorPlay.run_task(window, params, roundNum, totalCoins, Df, mini_df, summary_df, io, ser)

    roundNum += 1

Df, mini_df, summary_df = VAS.middle_vas(window, params, Df, mini_df, summary_df, roundNum, io)

Df, mini_df, summary_df = VAS.final_vas(window, params, Df, mini_df, summary_df, io)
DoorPlayInfra.show_screen_post_match(window, params, io, totalCoins, Df, mini_df)
helpers.graceful_quitting(window, params, Df, mini_df, summary_df)

# Recap
window.mouseVisible = True
core.quit()
