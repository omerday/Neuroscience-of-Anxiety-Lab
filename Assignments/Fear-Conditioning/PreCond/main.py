import os
import time

import json
from psychopy import visual
from psychopy.iohub.client.connect import launchHubServer
import configDialog
from psychopy import visual, core, event, monitors
import helpers
from psychopy.iohub.client.keyboard import Keyboard
import preCond
import conditioning
import test
import dataHadler
import VAS
import instructions
import serial
from serialHandler import *

io = launchHubServer()

debug = False
configDialogBank = configDialog.get_user_input(debug)

params = {
    "subject": configDialogBank[0],
    "session": configDialogBank[1],
    "gender": configDialogBank[2],
    "language": configDialogBank[3],
    "recordPhysio": configDialogBank[4],
    "skipInstructions": configDialogBank[5],
    "phase": configDialogBank[6],
    "version": configDialogBank[7],
    "faceCombinationIndex": configDialogBank[8],
    "faceCombination": helpers.FACE_COMBINATIONS[configDialogBank[8] - 1],
    "testRepetitions": 10,      # Amount of repetitions for each stimulus
    "shapes": ['square', 'circle', 'triangle', 'rhombus'],
    "natural": ['N1_F', 'N2_F', 'N3_F', 'N4_F', 'N5_M', 'N6_M', 'N7_M', 'N8_M'],
    "angry": ['A1_F', 'A2_F', 'A3_F', 'A4_F', 'A5_M', 'A6_M', 'A7_M', 'A8_M'],
    "plusDurationMin": 2,
    "plusDurationMax": 4,
    "shapeDuration": 10,
    "blockDuration": 24, # Not relevant, used in long version
    "relaxSlideDuration": 12,
    "blankSlideDuration": 15,
    "faceDurationMin": 8,
    "faceDurationMax": 9,
    "faceDurationTest": 8,
    "ITIDurationCondMin": 10,
    "ITIDurationCondMax": 12,
    "ITIDurationTestMin": 4,
    "ITIDurationTestMax": 6,
    "testBlockDuration": 18, # Not relevant, used in long version
    'port': 'COM4',
    'fullScreen': True,
    'startTime': time.time(),
}

dataHadler.export_face_combination(params)

if not os.path.exists("./data"):
    os.mkdir("data")
with open("./data/FCconfig.json", 'w') as file:
    json.dump(params, file, indent=3)

df_mood = dataHadler.setup_data_frame()
params['serialBiopac'] = serial.Serial(params['port'], 115200, bytesize=serial.EIGHTBITS, timeout=1) if params[
    'recordPhysio'] else None

# window
window = visual.Window(monitor="testMonitor", color="#C2E2FA", fullscr=params['fullScreen'])
window.mouseVisible = False
window.flip()

core.wait(0.5)

keyboard = io.devices.keyboard

# first slide before VAS
helpers.show_slide_and_wait(window, params, df_mood, io, keyboard, f"./img/instructions/start_{params['language'][0]}.jpg",
                    params['relaxSlideDuration'], True)

# First mood VAS
if params['recordPhysio']:
    report_event(params['serialBiopac'], BIOPAC_EVENTS['PreVas_rating'])

scores = VAS.run_vas(window, io, params, 'mood', mood_df=df_mood)
df_mood = dataHadler.insert_data_mood("pre", scores, df_mood)
dataHadler.save_backup(params, Mood=df_mood)

# Main experiment flow
lang_suf = 'E' if params['language'] == 'English' else 'H'
is_short_version = params['version'] == 'Short'
img_ext = ".jpeg" if is_short_version else ".jpg"

if params['phase'] == "Conditioning":
    # Instructions
    helpers.show_slide_and_wait(window, params, df_mood, io, keyboard, f"./img/instructions/instructions_{lang_suf}_1{img_ext}",
                        params['relaxSlideDuration'], True)
    helpers.show_slide_and_wait(window, params, df_mood, io, keyboard, f"./img/instructions/instructions_{lang_suf}_2{img_ext}",
                        params['relaxSlideDuration'], True)

    # Blank slide
    helpers.show_blank_slide_and_wait(window, params, df_mood, keyboard, io)

    # Pre-conditioning
    if params['recordPhysio']:
        report_event(params['serialBiopac'], BIOPAC_EVENTS['preCond'])
    preCond.pre_cond(params, window, io, keyboard, df_mood)

    # Conditioning
    if is_short_version:
        if params['recordPhysio']:
            report_event(params['serialBiopac'], BIOPAC_EVENTS['condNewVersion'])
        conditioning.condition_short_version(params, window, io, keyboard, df_mood)
    else:
        if params['recordPhysio']:
            report_event(params['serialBiopac'], BIOPAC_EVENTS['cond'])
        conditioning.condition_long_version(params, window, io, keyboard, df_mood)

    # Post-task VAS
    if params['recordPhysio']:
        report_event(params['serialBiopac'], BIOPAC_EVENTS['PostVas_rating'])
    scores = VAS.run_vas(window, io, params, 'mood', mood_df=df_mood)
    df_mood = dataHadler.insert_data_mood("post", scores, df_mood)

    # Final instruction
    helpers.show_slide_and_wait(window, params, df_mood, io, keyboard, f"./img/instructions/instructions_{lang_suf}_3.jpg",
                        params['relaxSlideDuration'], True)

elif params['phase'] == "Test":
    # Instruction
    helpers.show_slide_and_wait(window, params, df_mood, io, keyboard, f"./img/instructions/instructions_{lang_suf}_4{img_ext}",
                        params['relaxSlideDuration'], True)

    # Blank slide
    helpers.show_blank_slide_and_wait(window, params, df_mood, keyboard, io)

    # Test phase
    if is_short_version:
        if params['recordPhysio']:
            report_event(params['serialBiopac'], BIOPAC_EVENTS['testNewVersion'])
        test.test_short_version(params, window, io, keyboard, df_mood)
    else:
        if params['recordPhysio']:
            report_event(params['serialBiopac'], BIOPAC_EVENTS['test'])
        test.test_long_version(params, window, io, keyboard, df_mood)

    # Post-task VAS
    if params['recordPhysio']:
        report_event(params['serialBiopac'], BIOPAC_EVENTS['PostVas_rating'])
    scores = VAS.run_vas(window, io, params, 'mood', mood_df=df_mood)
    df_mood = dataHadler.insert_data_mood("post", scores, df_mood)

    # More slides
    helpers.show_slide_and_wait(window, params, df_mood, io, keyboard,
                        f"./img/instructions/instructions_{lang_suf}_5{img_ext}",
                        params['blankSlideDuration'], True)
    helpers.show_blank_slide_and_wait(window, params, df_mood, keyboard, io)
    helpers.show_slide_and_wait(window, params, df_mood, io, keyboard, f"./img/instructions/finish_{lang_suf}{img_ext}",
                        params['relaxSlideDuration'], True)

dataHadler.export_data(params, df_mood=df_mood)
# end of the study
helpers.wait_for_space(window, params, df_mood, io)
helpers.graceful_shutdown(window, params, df_mood)
