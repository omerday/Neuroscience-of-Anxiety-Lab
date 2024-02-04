import os
import random

import pretestVideos
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
    "gender": configDialogBank[3],
    "language": configDialogBank[4],
    'sequences': ["PNUNUNP", "UNPNPNU"],
    "sequenceOrder": configDialogBank[5],
    "shockType": configDialogBank[6],
    "skipStartle": configDialogBank[7],
    "recordPhysio": configDialogBank[8],
    "skipInstructions": configDialogBank[9],
    "skipCalibration": configDialogBank[10],
    'showVideos': configDialogBank[11],
    "fullScreen": configDialogBank[12] if debug is True else True,
    "saveDataAtQuit": configDialogBank[13] if debug is True else True,
    "saveConfig": configDialogBank[14] if debug is True else True,
    "screenSize": (1024, 768),
    "startTime": time.time(),
    'videoRestTime': 60,
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

videos_timing = random.choice(['Start', 'End'])
if params['showVideos'] and videos_timing == 'Start':
    pretestVideos.run_post_videos(window, params, io, ser)

image = visual.ImageStim(win=window, image=f"./img/instructions/1{params['gender'][0]}{params['language'][0]}.jpeg",
                         units="norm", opacity=1,
                         size=(2, 2))
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
fear_level = 5
sounds_in_order = helpers.randomize_sounds()
for ch in params["sequences"][params["sequenceOrder"] - 1]:
    fear_level, df, mini_df = blocksInfra.run_condition(window, image, params, io, ch, df, mini_df, 1, ser, fear_level, sounds_in_order[0] if ch != 'N' else None)
    df = instructionsScreen.blank_screen(window, image, params, df, io, 1, ch)
    if ch != 'N':
        sounds_in_order.pop(0)

if params['blocks'] == 2:
    # Additional Data Measuring
    if not params["skipCalibration"]:
        df, mini_df = instructionsScreen.midpoint(params, window, image, io, df, mini_df, ser)

    df, mini_df = VAS.vas(window, params, df, mini_df, io, 2)
    df = instructionsScreen.start_screen(window, image, params, df, io)

    fear_level = 5
    # Run Sequence #2
    sounds_in_order = helpers.randomize_sounds()
    for ch in params["sequences"][2 - params["sequenceOrder"]]:
        fear_level, df, mini_df = blocksInfra.run_condition(window, image, params, io, ch, df, mini_df, 2, ser, fear_level, sounds_in_order[0] if ch != 'N' else None)
        df = instructionsScreen.blank_screen(window, image, params, df, io, 2, ch)
        if ch != 'N':
            sounds_in_order.pop(0)

df, mini_df = VAS.vas(window, params, df, mini_df, io, 3)

# Show Post-Task Videos
if params['showVideos'] and videos_timing == 'End':
    pretestVideos.run_post_videos(window, params, io, ser)

# End of task Finalization
df, mini_df = instructionsScreen.finalization(params, window, image, io, df, mini_df)

dataHandler.export_data(params=params, fullDF=df, miniDF=mini_df)
