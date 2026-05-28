import os

from psychopy import gui
import json


def get_user_input(debug=False):
    """
    Gathers initial configuration for the Fort experiment.
    Simplified from NPU: blocks are always 2, condition order is always randomized.
    """

    loadedData = {}
    if os.path.exists("./data"):
        if os.path.exists("./data/FortConfig.json"):
            configExists = True
            with open("./data/FortConfig.json") as file:
                try:
                    loadedData = json.load(file)
                except json.decoder.JSONDecodeError:
                    configExists = False
        else:
            configExists = False
    else:
        os.mkdir("data")
        configExists = False

    userInput = gui.Dlg(title="Fort Task Configuration")
    userInput.addField('Subject Number:', )
    userInput.addField('Session:', 1)
    userInput.addField('Gender', "Female" if not configExists else loadedData.get("gender", "Female"),
                       choices=["Male", "Female"])
    userInput.addField("Preferred Language", "Hebrew" if not configExists else loadedData.get("language", "Hebrew"),
                       choices=["Hebrew", "English"])
    userInput.addField("Shock Type", "Sound" if not configExists else loadedData.get("shockType", "Sound"),
                       choices=["Shock", "Sound"])
    userInput.addField("Skip Startles", False if not configExists else loadedData.get("skipStartle", False))
    userInput.addField('Record Physiology', True if not configExists else loadedData.get('recordPhysio', True))
    userInput.addField('Skip Instructions', False if not configExists else loadedData.get('skipInstructions', False))
    userInput.addField('Skip Calibration', False if not configExists else loadedData.get('skipCalibration', False))
    userInput.addField('Calibration 1 Duration (sec)', 2 if not configExists else loadedData.get('calibrationTime1', 2))
    userInput.addField('Calibration 2 Duration (sec)', 2 if not configExists else loadedData.get('calibrationTime2', 2))
    userInput.addField('Calibration 3 Duration (sec)', 2 if not configExists else loadedData.get('calibrationTime3', 2))
    if debug:
        userInput.addField('Full Screen', True if not configExists else loadedData.get('fullScreen', True))
        userInput.addField('Save Data at Unexpected Quit', False if not configExists else loadedData.get('saveDataAtQuit', False))
        userInput.addField('Save Config as Default', False if not configExists else loadedData.get('saveConfig', False))
    return userInput.show()
