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
    "shapes": ['square', 'circle', 'triangle', 'rhombus'],
    "plusDurationMin": 2,
    "plusDurationMax": 4,
    "shapeDurationMin": 8,
    "shapeDurationMax": 9,
    "blockDuration": 24,
    "relaxSlideDuration": 12,
    "blankSlideDuration": 30,


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






