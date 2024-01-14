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
    userInput.addField('# of Blocks:', 1 if not configExists else loadedData['blocks'] - 1, choices=[1, 2]) # -1 because this is an index and not the value!
    userInput.addField('Gender', "Female" if not configExists else loadedData["gender"], choices=["Male", "Female"])
    userInput.addField("Preferred Language", "Hebrew" if not configExists else loadedData["language"],
                       choices=["Hebrew", "English"])
    userInput.addField('Conditions Sequence', 0 if not configExists else loadedData["sequenceOrder"] - 1,   # -1 because this is an index and not the value!
                       choices=[1, 2])
    userInput.addField("Shock Type", "Sound" if not configExists else loadedData["shockType"], choices=["Shock", "Sound"])
    userInput.addField("Skip Startles", False if not configExists else loadedData["skipStartle"])
    userInput.addField('Record Physiology', False if not configExists else loadedData['recordPhysio'])
    userInput.addField('Skip Instructions', False if not configExists else loadedData['skipInstructions'])
    userInput.addField('Skip Calibration', False if not configExists else loadedData['skipCalibration'])
    userInput.addField('Show Videos Before Task', False if not configExists else loadedData['showVideos'])
    if debug:
        userInput.addField('Full Screen', True if not configExists else loadedData['fullScreen'])
        userInput.addField('Save Data at Unexpected Quit', False if not configExists else loadedData['saveDataAtQuit'])
        userInput.addField('Save Config as Default', False if not configExists else loadedData['saveConfig'])
    # userInput.addField('Sound Mode:',choices=['PTB','Others'])
    return userInput.show()