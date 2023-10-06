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
from Assignments.Doors import DoorPlayInfra
from instructionsScreen import show_instructions
import VAS
import serial

io = launchHubServer()

# log = LoggerSetup.set_up_logger()
debug = False
configDialogBank = runConfigDialog.user_input_play(debug)

params = {
    'subjectID': configDialogBank[0],
    'Session': configDialogBank[1],
    'practiceTrials': configDialogBank[2],  # Number if Practice Trials, taken from Config Dialog
    'numOfDoors': configDialogBank[3],  # Number of Screens in the 1st task, either 49 (7*7) or 36 (6*6)
    'numOfTasks': configDialogBank[4],
    'startingDistance': configDialogBank[5],  # Decide whether the starting distance is random, or fixed on 50
    'recordPhysio': configDialogBank[6],
    'sensitivity': configDialogBank[7],
    'keyboardMode': configDialogBank[8],
    'screenSize': (1024, 768),  # Get Screen Resolution to match Full Screen
    'soundOn': configDialogBank[9],
    'skipInstructions': configDialogBank[10],
    'language': configDialogBank[11],
    'fullScreen': configDialogBank[12] if debug else True,
    'saveDataAtQuit': configDialogBank[13] if debug else True,
    'startTime': time.time(),
    'saveAsDefault': configDialogBank[14] if debug else True,
    'doorImagePathPrefix': './img/doors1/',
    'outcomeImagePredix': './img/outcomes/',
    'imageSuffix': '.jpg',
    'port': 'COM4',
}

if params['saveAsDefault']:
    with open("./data/config.json", 'w') as file:
        json.dump(params, file, indent=3)

# Initialize serial port
ser = serial.Serial(params['port'], 115200, bytesize=serial.EIGHTBITS, timeout=1) if params['recordPhysio'] else None
if params['recordPhysio']:
    serialHandler.report_event(ser, 255)

# Initialize DataFrame
params, Df, miniDf = dataHandler.setup_data_frame(params)

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
Df, miniDf = VAS.beginning_vas(window, params, Df, miniDf)

if not params['skipInstructions']:

    # Show Instructions
    Df, miniDf = show_instructions(window, params, image, Df, miniDf, io)

    # Practice run
    Df, miniDf = DoorPlay.practice_run(window, params, Df, miniDf, io, ser)

# Task 1
Df, miniDf, totalCoins = DoorPlay.run_task(window, params, 1, 0, Df, miniDf, io, ser)

roundNum = 2
while roundNum <= params['numOfTasks']:
    # Mid-VAS
    Df, miniDf = VAS.middle_vas(window, params, Df, miniDf, roundNum)

    # Task 2
    Df, miniDf, totalCoins = DoorPlay.run_task(window, params, roundNum, totalCoins, Df, miniDf, io, ser)

    roundNum += 1

Df, miniDf = VAS.middle_vas(window, params, Df, miniDf, roundNum)

# Final VAS
Df, miniDf = VAS.final_vas(window, params, Df, miniDf)
DoorPlayInfra.show_screen_post_match(window, params, io, totalCoins)
helpers.graceful_quitting(window, params, Df, miniDf)

# Recap
window.mouseVisible = True
core.quit()
