import os

from psychopy import gui
import json


def get_user_input(debug=False):
    """
    In charge of gathering initial info for configuration using gui.Dlg. it's being inserted into Params dictionary in
    the main file.
    :return: answer array
    """

    loadedData = {}
    if os.path.exists("./data"):
        if os.path.exists("./data/NPUconfig.json"):
            configExists = True
            with open("./data/NPUconfig.json") as file:
                try:
                    loadedData = json.load(file)
                except json.decoder.JSONDecodeError:
                    configExists = False
        else:
            configExists = False
    else:
        os.mkdir("data")
        configExists = False

    userInput = gui.Dlg(title="NPU Task Configuration")
    userInput.addField('Subject Number:', )
    userInput.addField('Session:', 1)
    userInput.addField('# of Blocks:', 2 if not configExists else loadedData['blocks'] - 1, choices=[1, 2, 3])
    userInput.addField('Gender', "Female" if not configExists else loadedData["gender"], choices=["Male", "Female"])
    userInput.addField("Preferred Language", "Hebrew" if not configExists else loadedData["language"],
                       choices=["Hebrew", "English"])
    userInput.addField('First Block Order', "PNUNUNP" if not configExists else loadedData["firstBlock"],
                       choices=["PNUNUNP", "UNPNPNU"])
    userInput.addField('Second Block Order', "UNPNPNU" if not configExists else loadedData["secondBlock"],
                       choices=["PNUNUNP", "UNPNPNU"])
    userInput.addField("Shock Type", "Shock" if not configExists else loadedData["shockType"], choices=["Shock", "Sound"])
    userInput.addField("Skip Startles", False if not configExists else loadedData["skipStartle"])
    userInput.addField('Record Physiology', False if not configExists else loadedData['recordPhysio'])
    userInput.addField('Skip Instructions', False if not configExists else loadedData['skipInstructions'])
    userInput.addField('Skip Calibration', False if not configExists else loadedData['skipCalibration'])
    if debug:
        userInput.addField('Full Screen', True if not configExists else loadedData['fullScreen'])
        userInput.addField('Save Data at Unexpected Quit', False if not configExists else loadedData['saveDataAtQuit'])
        userInput.addField('Save Config as Default', False if not configExists else loadedData['saveConfig'])
    # userInput.addField('Sound Mode:',choices=['PTB','Others'])
    return userInput.show()