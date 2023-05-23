import time

import pandas
from psychopy import visual, core, event
import DoorPlay
import helpers
from psychopy.iohub import launchHubServer
import runConfigDialog
import dataHandler
from instructionsScreen import show_instructions
import VAS
import serial

io = launchHubServer()

# log = LoggerSetup.set_up_logger()
configDialogBank = runConfigDialog.user_input_play()

params = {
    'subjectID': configDialogBank[0],
    'practiceTrials': configDialogBank[1],  # Number if Practice Trials, taken from Config Dialog
    'numOfScreensTask1': configDialogBank[2],  # Number of Screens in the 1st task, either 49 (7*7) or 36 (6*6)
    'numOfScreensTask2': configDialogBank[3],  # Number of Screens in the 2nd task, either 49 (7*7) or 36 (6*6)
    'startingDistance': configDialogBank[4],  # Decide whether the starting distance is random, or fixed on 50
    'recordPhysio': configDialogBank[5],
    'sensitivity': configDialogBank[6],
    'fullScreen': configDialogBank[7],
    'keyboardMode': configDialogBank[8],
    'screenSize': (1024, 768),  # Get Screen Resolution to match Full Screen
    'saveDataAtQuit': configDialogBank[9],
    'startTime': time.time(),
    'saveAsDefault': configDialogBank[10],
    'doorImagePathPrefix': './img/doors1/',
    'outcomeImagePredix': './img/outcomes/',
    'imageSuffix': '.jpg',
    'port': 'COM4',
}

# Initialize serial port
ser = serial.Serial(params['port'], 115200, bytesize=serial.EIGHTBITS) if params['recordPhysio'] else None

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
# Df, miniDf = VAS.beginning_vas(window, params, Df, miniDf)

# Show Instructions
# Df, miniDf = show_instructions(window, params, image, Df, miniDf, io)

# Practice run
Df, miniDf = DoorPlay.practice_run(window, params, Df, miniDf, io, ser)

# Task 1
Df, miniDf, totalCoins = DoorPlay.run_task(window, params, 1, 0, Df, miniDf, io, ser)

# Mid-VAS
Df, miniDf = VAS.middle_vas(window, params, 0, Df, miniDf)

# Task 2
Df, miniDf, totalCoins = DoorPlay.run_task(window, params, 2, totalCoins, Df, miniDf, io, ser)

# Final VAS
Df, miniDf = VAS.final_vas(window, params, Df, miniDf)
dataHandler.export_summarized_dataframe(params, miniDf)

# Recap
window.mouseVisible = True
core.quit()
