"""
קונפיג

שקף התחלה

שאלות vas

הוראות - שקף 1

חצי דקה מסך ריק (שקף מרני)

precond

cond

הוראות - שקף 2

doors

הוראות - שקף 3

test

vas

שקף ריק??

שקף סיום
"""
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
import cond
import test
import cond
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
    "preCond": configDialogBank[6],
    "test": configDialogBank[7],
    "shapes": ['square', 'circle', 'triangle', 'rhombus'],
    "natural": ['N1_F', 'N2_F', 'N3_F', 'N4_F', 'N5_M', 'N6_M', 'N7_M', 'N8_M'],
    "angry": ['A1_F', 'A2_F', 'A3_F', 'A4_F', 'A5_M', 'A6_M', 'A7_M', 'A8_M'],
    "plusDurationMin": 2,
    "plusDurationMax": 4,
    "shapeDurationMin": 8,
    "shapeDurationMax": 9,
    "blockDuration": 24,
    "relaxSlideDuration": 12,
    "blankSlideDuration": 30,
    "faceDurationMin": 8,
    "faceDurationMax": 9,
    "testBlockDuration": 18,
    'port': 'COM4',
    'fullScreen': True,
    'startTime': time.time(),
}


if not os.path.exists("./data"):
    os.mkdir("data")
with open("./data/FCconfig.json", 'w') as file:
    json.dump(params, file, indent=3)

df_mood = dataHadler.setup_data_frame()
params['serialBiopac'] = serial.Serial(params['port'], 115200, bytesize=serial.EIGHTBITS, timeout=1) if params[
    'recordPhysio'] else None


# window
window = visual.Window(monitor="testMonitor", fullscr=params['fullScreen'], color=(210, 210, 210))
window.mouseVisible = False
window.flip()

core.wait(0.5)

keyboard = io.devices.keyboard


# First mood VAS
if params['recordPhysio']:
    report_event(params['serialBiopac'], BIOPAC_EVENTS['PreVas_rating'])

# first slide before VAS - שקף התחלה - 27/3
display_time = params['relaxSlideDuration']
start = visual.ImageStim(window, image=f"./img/instructions/start_{params['language'][0]}.jpeg", units="norm", size=(2, 2))
start.draw()
window.mouseVisible = False
window.flip()
start_time = time.time()
helpers.wait_for_space(window, params, df_mood, io)

scores = VAS.run_vas(window, io, params, 'mood', mood_df=df_mood)
df_mood = dataHadler.insert_data_mood("pre", scores, df_mood)

if params['preCond']:
    """ if not params['skipInstructions']:
            instructions.instructions(window, params, io)"""

    # הוראות שקף 1 - 27/3
    display_time = params['relaxSlideDuration']
    instructions_1 = visual.ImageStim(window, image=f"./img/instructions/instructions_{'E' if params['language'] == 'English' else 'H'}_1.jpeg", units="norm", size=(2, 2))
    instructions_1.draw()
    window.mouseVisible = False
    window.flip()
    start_time = time.time()
    helpers.wait_for_space(window, params, df_mood, io)

    # 30 seconds relaxing - no need 29/3
    """ display_time = params['relaxSlideDuration']
    relax = visual.ImageStim(window, image=f"./img/relax_slide.jpeg", units="norm", size=(2, 2))
    relax.draw()
    window.mouseVisible = False
    window.flip()
    start_time = time.time()
    helpers.wait_for_time(window, params, start_time, display_time, keyboard) """

    display_time = params['blankSlideDuration']
    blank = visual.ImageStim(window, image=f"./img/blank.jpeg", units="norm", size=(2, 2))
    blank.draw()
    window.mouseVisible = False
    window.flip()
    start_time = time.time()
    helpers.wait_for_time(window, params, df_mood, start_time, display_time, keyboard)

    if params['recordPhysio']:
        report_event(params['serialBiopac'], BIOPAC_EVENTS['preCond'])

    # calling the preCond function
    preCond.pre_cond(params, window, io, keyboard, df_mood)

    if params['recordPhysio']:
        report_event(params['serialBiopac'], BIOPAC_EVENTS['cond'])

    # calling the cond function
    cond.cond(params, window, io, keyboard, df_mood)

    # Last mood VAS
    if params['recordPhysio']:
        report_event(params['serialBiopac'], BIOPAC_EVENTS['PostVas_rating'])
    scores = VAS.run_vas(window, io, params, 'mood', mood_df=df_mood)
    df_mood = dataHadler.insert_data_mood("post", scores, df_mood)

    # שקף 2
    display_time = params['relaxSlideDuration']
    image = visual.ImageStim(window,
                             image=f"./img/instructions/instructions_{'E' if params['language'] == 'English' else 'H'}_2.jpeg",
                             units="norm", size=(2, 2))
    image.draw()
    window.mouseVisible = False
    window.flip()
    start_time = time.time()
    helpers.wait_for_time(window, params, df_mood, start_time, display_time, keyboard)


if params['test']:
    """ if not params['skipInstructions']:
            instructions.instructions(window, params, io) """

    # הוראות - שקף 3 - 27/3
    display_time = params['relaxSlideDuration']
    instructions_3 = visual.ImageStim(window,
                                      image=f"./img/instructions/instructions_{'E' if params['language'] == 'English' else 'H'}_3.jpeg",
                                      units="norm", size=(2, 2))
    instructions_3.draw()
    window.mouseVisible = False
    window.flip()
    start_time = time.time()
    helpers.wait_for_space(window, params, df_mood, io)

    # 30 seconds relaxing - no need
    """ display_time = params['relaxSlideDuration']
    relax = visual.ImageStim(window, image=f"./img/relax_slide.jpeg", units="norm", size=(2, 2))
    relax.draw()
    window.mouseVisible = False
    window.flip()
    start_time = time.time()
    helpers.wait_for_time(window, params, start_time, display_time, keyboard) """

    display_time = params['blankSlideDuration']
    blank = visual.ImageStim(window, image=f"./img/blank.jpeg", units="norm", size=(2, 2))
    blank.draw()
    window.mouseVisible = False
    window.flip()
    start_time = time.time()
    helpers.wait_for_time(window, params, df_mood, start_time, display_time, keyboard)

    # calling the test function
    test.test(params, window, io, keyboard, df_mood)

    # Last mood VAS
    if params['recordPhysio']:
        report_event(params['serialBiopac'], BIOPAC_EVENTS['PostVas_rating'])
    scores = VAS.run_vas(window, io, params, 'mood', mood_df=df_mood)
    df_mood = dataHadler.insert_data_mood("post", scores, df_mood)

    # שקף סיום
    display_time = params['relaxSlideDuration']
    image = visual.ImageStim(window,
                             image=f"./img/instructions/finish_{'E' if params['language'] == 'English' else 'H'}.jpeg",
                             units="norm", size=(2, 2))
    image.draw()
    window.mouseVisible = False
    window.flip()
    start_time = time.time()
    helpers.wait_for_time(window, params, df_mood, start_time, display_time, keyboard)


# end of the study
helpers.wait_for_space(window, params, df_mood, io)
helpers.graceful_shutdown(window, params, df_mood)






