import os
from psychopy.iohub import launchHubServer
from psychopy import visual, core, event, monitors
import configDialog
import json
import helpers, instructionsScreen

io = launchHubServer()

debug = False
configDialogBank = configDialog.get_user_input(debug)

params = {
    "Subject": configDialogBank[0],
    "session": configDialogBank[1],
    "blocks": configDialogBank[2],
    "gender": "F" if configDialogBank[3] == "Female" else "M",
    "language": configDialogBank[4],
    "shockType": configDialogBank[5],
    "timing": configDialogBank[6],
    "recordPhysio": configDialogBank[7],
    "skipInstructions": configDialogBank[8],
    "fullScreen": configDialogBank[9] if debug is True else True,
    "saveDataAtQuit": configDialogBank[10] if debug is True else True,
    "saveConfig": configDialogBank[11] if debug is True else True,
    "screenSize": (1024, 768)
}

if params['saveConfig']:
    if not os.path.exists("./data"):
        os.mkdir("data")
    with open("./data/config.json", 'w') as file:
        json.dump(params, file, indent=3)

window = visual.Window(size=params['screenSize'], monitor="testMonitor", color="black", winType='pyglet',
                       fullscr=True if params['fullScreen'] else False, units="pix")
image = visual.ImageStim(win=window, image="./img/init.jpg", units="norm", opacity=1,
                         size=(2, 2) if not params['fullScreen'] else None)
image.draw()
window.mouseVisible = False
window.update()
helpers.wait_for_space(window, io)

# Initiate instructions sequence
if not params["skipInstructions"]:
    instructionsScreen.show_instructions(params, window, image, io)

# Run Sequence

# Additional Data Measuring
instructionsScreen.midpoint(params, window, image, io)

# Run Sequence #2

# End of task Finalization
instructionsScreen.finalization(params, window, image, io)