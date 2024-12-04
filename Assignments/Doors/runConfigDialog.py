import os

from psychopy import gui
import json


def user_input_play(debug=False):
    """
    In charge of gathering initial info for configuration using gui.Dlg. it's being inserted into Params dictionary in
    the main file.
    :return: answer array
    """

    loadedData = {}
    if os.path.exists("./data"):
        if os.path.exists("./data/doorsConfig.json"):
            configExists = True
            with open("./data/doorsConfig.json") as file:
                try:
                    loadedData = json.load(file)
                except json.decoder.JSONDecodeError:
                    configExists = False
        else:
            configExists = False
    else:
        os.mkdir("data")
        configExists = False

    userInput = gui.Dlg(title="DOORS Task Information")
    userInput.addField('Subject Number', )
    userInput.addField('Session', 1)
    # userInput.addField('Version:', choices=[1, 2])
    userInput.addField('# of Doors', choices=["49", "36 (6x6)", "36 (7x7)"])
    userInput.addField('# of Runs', 1 if not configExists else loadedData['numOfTasks'] - 1, choices=[1, 2, 3])
    userInput.addField('Starting Distance', choices=[50,'40-60', 'Random'])
    userInput.addField('Record Physiology', False if not configExists else loadedData['recordPhysio'])
    userInput.addField('Sensitivity (2: Less sensitive, 3: Normal, 4: More sensitive)', 1 if not configExists else loadedData['sensitivity'] - 2, choices=[2, 3, 4])
    userInput.addField("Door Layout", "P - R" if not configExists else loadedData['doorLayout'],
                       choices=["P - R", "R - P"])
    userInput.addField('Keyboard Mode', True if not configExists else loadedData['keyboardMode'])
    userInput.addField('Sound On?', True if not configExists else loadedData['soundOn'])
    userInput.addField("Variation", "None", choices=["None", "SCR", "CAM", "HV"])
    userInput.addField("Order", "NEUT-ACT", choices=["NEUT-ACT", "ACT-NEUT"])
    userInput.addField('Skip Instructions', False if not configExists else loadedData['skipInstructions'])
    userInput.addField("Preferred Language", "Hebrew" if not configExists else loadedData["language"], choices=["Hebrew", "English"])
    if debug:
        userInput.addField('Full Screen', True if not configExists else loadedData['fullScreen'])
        userInput.addField('Save Data at Unexpected Quit', False if not configExists else loadedData['saveDataAtQuit'])
        userInput.addField('Save Config as Default', False if not configExists else loadedData['saveAsDefault'])
    # userInput.addField('Sound Mode:',choices=['PTB','Others'])
    return userInput.show()
