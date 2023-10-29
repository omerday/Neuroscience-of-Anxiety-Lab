import os

import configDialog
import json

debug = True
configDialogBank = configDialog.get_user_input(debug)

params = {
    "subjectID": configDialogBank[0],
    "session": configDialogBank[1],
    "blocks": configDialogBank[2],
    "recordPhysio": configDialogBank[3],
    "skipInstructions": configDialogBank[4],
    "gender": "F" if configDialogBank[5] == "Female" else "M",
    "language": configDialogBank[6],
    "fullScreen": configDialogBank[7] if debug is True else True,
    "saveDataAtQuit": configDialogBank[8] if debug is True else True,
    "saveConfig": configDialogBank[9] if debug is True else True
}

if params['saveConfig']:
    if not os.path.exists("./data"):
        os.mkdir("data")
    with open("./data/config.json", 'w') as file:
        json.dump(params, file, indent=3)

print(params)