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

# Parameters and configurations for the task:
params = {
    'Subject': configDialogBank[0],
    'Session': configDialogBank[1],
    'practiceTrials': 1,                        # Number if Practice Trials, taken from Config Dialog
    'numOfDoors': configDialogBank[2],          # Number of Screens in every task, either 49 (7*7) or 36 (6*6)
    'numOfSimulationDoors': 5,                  # Amount of doors to be presented in the simulation part during the instructions
    'numOfTasks': configDialogBank[3],          # Number of Sessions (each consisting of 36-49 doors)
    'startingDistance': configDialogBank[4],    # Decide whether the starting distance is random, or fixed on 50
    'recordPhysio': configDialogBank[5],
    'sensitivity': configDialogBank[6],         # Size of each step getting closer/further from the door
    'doorLayout': configDialogBank[7],          # Decides whether the punishment is on the left or on the right
    'ITIDurationMin': 1,                        # Two parameters to set the duration of the in-between-doors video
    'ITIDurationMax': 2.5,
    'keyboardMode': configDialogBank[8],
    'screenSize': (1024, 768),                  # Get Screen Resolution to match Full Screen
    'soundOn': configDialogBank[9],
    'beeps': False,                             # An option to sound beeps before the door outcome is presented
    'outcomeString': True,   # True if we want to print the outcome amount, otherwise it will just show a monster / a fairy
    'screamVersion': True if configDialogBank[10] == "SCR" else False,
    'cameraVersion': True if configDialogBank[10] == "CAM" else False,
    'highValue': True if configDialogBank[10] == "HV" else False,
    'ACTBlock': 1 if configDialogBank[11] == "ACT-NEUT" else 2,
    'skipInstructions': configDialogBank[12],
    'language': configDialogBank[13],
    'reducedEvents': False,                      # Send only one event for each doors (door presented), instead of three - door presented, locked and outcome
    'fullScreen': configDialogBank[14] if debug else True,
    'saveDataAtQuit': configDialogBank[15] if debug else True,
    'startTime': time.time(),
    'saveAsDefault': configDialogBank[16] if debug else True,
    'doorImagePathPrefix': './img/doors1/' if configDialogBank[8] == "P - R" else './img/doors2/',
    'doorOutcomePath': './img/outcomes/',
    'imageSuffix': '.jpg',
    'port': 'COM4',
}

# Save parameters backup to be used as default settings in the next run
if params['saveAsDefault']:
    if not os.path.exists("./data"):
        os.mkdir("data")
    with open("./data/doorsConfig.json", 'w') as file:
        json.dump(params, file, indent=3)

# Initialize serial port for BioPac Communication
ser = serial.Serial(params['port'], 115200, bytesize=serial.EIGHTBITS, timeout=1) if params['recordPhysio'] else None
if params['recordPhysio']:
    serialHandler.report_event(ser, 255)

# Initialize DataFrame
params, mini_df, summary_df = dataHandler.setup_data_frame(params)

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
mini_df, summary_df = VAS.beginning_vas(window, params, mini_df, summary_df, io)

if not params['skipInstructions']:

    # Show Instructions, practice trial and the simulation
    mini_df, summary_df = show_instructions(window, params, mini_df, summary_df, io, ser)

# Task 1
mini_df, summary_df, totalCoins = DoorPlay.run_task(window, params, 1, 0, mini_df, summary_df, io, ser)

roundNum = 2
while roundNum <= params['numOfTasks']:
    # Mid-VAS
    mini_df, summary_df = VAS.middle_vas(window, params, mini_df, summary_df, roundNum, io)

    # Task 2
    mini_df, summary_df, totalCoins = DoorPlay.run_task(window, params, roundNum, 0, mini_df, summary_df, io, ser)

    roundNum += 1

mini_df, summary_df = VAS.middle_vas(window, params, mini_df, summary_df, roundNum, io)

mini_df, summary_df = VAS.final_vas(window, params, mini_df, summary_df, io)
DoorPlayInfra.show_screen_post_match(window, params, io, totalCoins, mini_df)
helpers.graceful_quitting(window, params, mini_df, summary_df)

# Recap
window.mouseVisible = True
core.quit()
