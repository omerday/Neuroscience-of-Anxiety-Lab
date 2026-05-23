import os
import random
import json
import time

import pandas as pd
import serial
from psychopy.iohub import launchHubServer
from psychopy import visual, core

import configDialog
import helpers
import instructionsScreen
import blocksInfra
import dataHandler
import VAS
import serialHandler

# ---------------------------------------------------------------------------
# Fort Experiment Flow
#
#   1. Instructions (same as NPU)
#   2. Calibration / startle habituation (~1 min, same as NPU)
#   3. VAS round 1 (participant state questions)
#   4. Start screen
#   5. Block 1: N/P/U in randomized order
#   6. VAS round 2
#   7. 5-minute break screen
#   8. Block 2: N/P/U in a new randomized order
#   9. VAS round 3
#  10. Data export + finalization
# ---------------------------------------------------------------------------

io = launchHubServer()

debug = False
configDialogBank = configDialog.get_user_input(debug)

# Map dialog fields to params (no blocks/sequenceOrder — always 2 blocks, always random order)
params = {
    "Subject": configDialogBank[0],
    "session": configDialogBank[1],
    "blocks": 2,
    "gender": configDialogBank[2],
    "language": configDialogBank[3],
    "shockType": configDialogBank[4],
    "skipStartle": configDialogBank[5],
    "recordPhysio": configDialogBank[6],
    "skipInstructions": configDialogBank[7],
    "calibrationTime": 2,
    "skipCalibration": configDialogBank[8],
    "fullScreen": configDialogBank[9] if debug is True else True,
    "saveDataAtQuit": configDialogBank[10] if debug is True else True,
    "saveConfig": configDialogBank[11] if debug is True else True,
    "screenSize": (1024, 768),
    "startTime": time.time(),
    "port": "COM4",
}

if params["saveConfig"]:
    if not os.path.exists("./data"):
        os.mkdir("data")
    with open("./data/FortConfig.json", "w") as file:
        json.dump(params, file, indent=3)

ser = serial.Serial(params["port"], 115200, bytesize=serial.EIGHTBITS, timeout=1) if params["recordPhysio"] else None
if params["recordPhysio"]:
    serialHandler.report_event(ser, 255)

window = visual.Window(
    size=params["screenSize"], monitor="testMonitor", color=(0.6, 0.6, 0.6),
    winType="pyglet", fullscr=True if params["fullScreen"] else False, units="pix"
)

image = visual.ImageStim(
    win=window,
    image=f"./img/instructions/Welcome_{params['gender'][0]}{params['language'][0]}.jpeg",
    units="norm", opacity=1, size=(2, 2)
)
image.draw()
window.update()
window.mouseVisible = False
helpers.wait_for_space_no_df(window, io)

# Setup data frames
params, df, mini_df = dataHandler.setup_data_frame(params)

params["startTime"] = time.time()
temp_dict = dataHandler.create_dict_for_df(params, Step="Start")
temp_dict["CurrentTime"] = 0.0
mini_df = pd.concat([mini_df, pd.DataFrame.from_records([temp_dict])])
del temp_dict

# 1. Instructions
if not params["skipInstructions"]:
    df, mini_df = instructionsScreen.show_instructions(params, window, image, io, df, mini_df, ser)

# 2. Calibration / startle habituation (~1 min)
if not params["skipStartle"]:
    df, mini_df = helpers.startle_habituation_sequence(window, image, params, io, df, mini_df, ser)

# 3. VAS round 1
df, mini_df = VAS.vas(window, params, df, mini_df, io, 1)

# 4. Start screen
df = instructionsScreen.start_screen(window, image, params, df, io)

# 5. Block 1 — random permutation of N, P, U
fear_level = 5
sounds_in_order = helpers.randomize_sounds()
block1_sequence = ["N", "P", "U"]
random.shuffle(block1_sequence)
print(f"Block 1 sequence: {block1_sequence}")

for ch in block1_sequence:
    fear_level, df, mini_df = blocksInfra.run_condition(
        window, image, params, io, ch, df, mini_df, 1, ser, fear_level,
        sounds_in_order[0] if ch != "N" else None
    )
    df = instructionsScreen.blank_screen(window, image, params, df, io, 1, ch)
    if ch != "N":
        sounds_in_order.pop(0)

# 6. VAS round 2
df, mini_df = VAS.vas(window, params, df, mini_df, io, 2)

# 7. 5-minute break screen
df, mini_df = instructionsScreen.break_screen(window, image, params, df, mini_df, io)

# 8. Block 2 — another random permutation of N, P, U
fear_level = 5
sounds_in_order = helpers.randomize_sounds()
block2_sequence = ["N", "P", "U"]
random.shuffle(block2_sequence)
print(f"Block 2 sequence: {block2_sequence}")

for ch in block2_sequence:
    fear_level, df, mini_df = blocksInfra.run_condition(
        window, image, params, io, ch, df, mini_df, 2, ser, fear_level,
        sounds_in_order[0] if ch != "N" else None
    )
    df = instructionsScreen.blank_screen(window, image, params, df, io, 2, ch)
    if ch != "N":
        sounds_in_order.pop(0)

# 9. VAS round 3
df, mini_df = VAS.vas(window, params, df, mini_df, io, 3)

# 10. Export + finalization
dataHandler.export_data(params=params, fullDF=df, miniDF=mini_df)

df, mini_df = instructionsScreen.finalization(params, window, image, io, df, mini_df)

dataHandler.export_data(params=params, fullDF=df, miniDF=mini_df)
