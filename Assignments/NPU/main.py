import os

import pandas as pd
from psychopy.iohub import launchHubServer
from psychopy import visual, core, event, monitors
import configDialog
import json
import helpers, instructionsScreen
import blocksInfra
import time
import dataHandler
import VAS
import serial, serialHandler

io = launchHubServer()

debug = False
configDialogBank = configDialog.get_user_input(debug)

params = {
    "Subject": configDialogBank[0],
    "session": configDialogBank[1],
    "blocks": configDialogBank[2],
    "gender": "F" if configDialogBank[3] == "Female" else "M",
    "language": configDialogBank[4],
    "firstBlock": configDialogBank[5],
    "secondBlock": configDialogBank[6],
    "shockType": configDialogBank[7],
    "skipStartle": configDialogBank[8],
    "recordPhysio": configDialogBank[9],
    "skipInstructions": configDialogBank[10],
    "skipCalibration": configDialogBank[11],
    "fullScreen": configDialogBank[12] if debug is True else True,
    "saveDataAtQuit": configDialogBank[13] if debug is True else True,
    "saveConfig": configDialogBank[14] if debug is True else True,
    "screenSize": (1024, 768),
    "startTime": time.time(),
    'port': 'COM4',
}

if params['saveConfig']:
    if not os.path.exists("./data"):
        os.mkdir("data")
    with open("./data/NPUconfig.json", 'w') as file:
        json.dump(params, file, indent=3)

ser = serial.Serial(params['port'], 115200, bytesize=serial.EIGHTBITS, timeout=1) if params['recordPhysio'] else None
if params['recordPhysio']:
    serialHandler.report_event(ser, 255)

window = visual.Window(size=params['screenSize'], monitor="testMonitor", color=(0.6, 0.6, 0.6), winType='pyglet',
                       fullscr=True if params['fullScreen'] else False, units="pix")
image = visual.ImageStim(win=window, image="./img/init.jpeg", units="norm", opacity=1,
                         size=(2, 2) if not params['fullScreen'] else None)
image.draw()
window.mouseVisible = False
window.update()
helpers.wait_for_space_no_df(window, io)

# Setup DFs
params, df, mini_df = dataHandler.setup_data_frame(params)

# Add First Line
params['startTime'] = time.time()
temp_dict = dataHandler.create_dict_for_df(params, Step="Start")
temp_dict["CurrentTime"] = 0.0
mini_df = pd.concat([mini_df, pd.DataFrame.from_records([temp_dict])])
del temp_dict

# Initiate instructions sequence
if not params["skipInstructions"]:
    df, mini_df = instructionsScreen.show_instructions(params, window, image, io, df, mini_df, ser)

if not params['skipStartle']:
    df, mini_df = helpers.startle_habituation_sequence(window, image, params, io, df, mini_df, ser)
df, mini_df = VAS.vas(window, params, df, mini_df, io, 1)
df = instructionsScreen.start_screen(window, image, params, df, io)

# Run Sequence
for ch in params["firstBlock"]:
    df, mini_df = blocksInfra.run_condition(window, image, params, io, ch, df, mini_df,1, ser)
    df = instructionsScreen.blank_screen(window, image, params, df, io, 1, ch)

# Additional Data Measuring
if not params["skipCalibration"]:
    df, mini_df = instructionsScreen.midpoint(params, window, image, io, df, mini_df, ser)

df, mini_df = VAS.vas(window, params, df, mini_df, io, 2)
df = instructionsScreen.start_screen(window, image, params, df, io)

# Run Sequence #2
for ch in params["secondBlock"]:
    df, mini_df = blocksInfra.run_condition(window, image, params, io, ch, df, mini_df,2, ser)
    df = instructionsScreen.blank_screen(window, image, params, df, io, 2, ch)

df, mini_df = VAS.vas(window, params, df, mini_df, io, 3)

# End of task Finalization
df, mini_df = instructionsScreen.finalization(params, window, image, io, df, mini_df)