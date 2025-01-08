"""
קונפיג

שאלות vas

הוראות

חצי דקה מסך ריק (שקף מרני)

precond

cond

vas

שקף ריק??
"""
import time

from psychopy import visual
from psychopy.iohub.client.connect import launchHubServer
import configDialog
from psychopy import visual, core, event, monitors
import helpers
from psychopy.iohub.client.keyboard import Keyboard
import preCond
import test

io = launchHubServer()

debug = False
configDialogBank = configDialog.get_user_input(debug)

params = {
    "subject": configDialogBank[0],
    "session": configDialogBank[1],
    "gender": configDialogBank[2],
    "language": configDialogBank[3],
    "recordPhysio": configDialogBank[4],
    "skipInstruction": configDialogBank[5],
    "preCond": configDialogBank[6],
    "test": configDialogBank[7],
    "shapes": ['square', 'circle', 'triangle', 'rhombus'],
    "natural": ['N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'N8'],
    "angry": ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8'],
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


}

# window
window = visual.Window(monitor="testMonitor", fullscr=params['fullScreen'], color=(210, 210, 210))
window.mouseVisible = False
window.flip()

core.wait(0.5)

keyboard = io.devices.keyboard

# TODO: First mood VAS
if params['recordPhysio']:
    report_event(params['serialBiopac'], BIOPAC_EVENTS['PreVas_rating'])
scores = run_vas(window, io, params, 'mood', mood_df=df_mood, pain_df=df_pain, device=device)
df_mood = insert_data_mood("pre", scores, df_mood)

if params['preCond']:
    # TODO: instructions
    if not params['skipInstructions']:
        instructions.instructions(window, params, io)

    # 30 seconds relaxing
    display_time = params['relaxSlideDuration']
    relax = visual.ImageStim(window, image=f"./img/relax_slide.jpeg", units="norm", size=(2, 2))
    relax.draw()
    window.mouseVisible = False
    window.flip()
    start_time = time.time()
    helpers.wait_for_time(window, params, start_time, display_time, keyboard)

    display_time = params['blankSlideDuration']
    blank = visual.ImageStim(window, image=f"./img/blank.jpeg", units="norm", size=(2, 2))
    blank.draw()
    window.mouseVisible = False
    window.flip()
    start_time = time.time()
    helpers.wait_for_time(window, params, start_time, display_time, keyboard)

    # calling the preCond function
    preCond.pre_cond(params, window, io, keyboard)

    # TODO: calling the cond function

if params['Test']:
    # TODO: instructions
    if not params['skipInstructions']:
        instructions.instructions(window, params, io)

    # 30 seconds relaxing
    display_time = params['relaxSlideDuration']
    relax = visual.ImageStim(window, image=f"./img/relax_slide.jpeg", units="norm", size=(2, 2))
    relax.draw()
    window.mouseVisible = False
    window.flip()
    start_time = time.time()
    helpers.wait_for_time(window, params, start_time, display_time, keyboard)

    display_time = params['blankSlideDuration']
    blank = visual.ImageStim(window, image=f"./img/blank.jpeg", units="norm", size=(2, 2))
    blank.draw()
    window.mouseVisible = False
    window.flip()
    start_time = time.time()
    helpers.wait_for_time(window, params, start_time, display_time, keyboard)

    # calling the test function
    test.test(params, window, io, keyboard)

# TODO: last mood VAS






