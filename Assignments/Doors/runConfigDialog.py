import os

from psychopy import gui
import json

def user_input_play():
    """
    In charge of gathering initial info for configuration using gui.Dlg. it's being inserted into Params dictionary in
    the main file.
    :return: answer array
    """

    loadedData = {}
    if os.path.exists("./data/config.json"):
        configExists = True
        with open("./data/config.json") as file:
            try:
                loadedData = json.load(file)
            except json.decoder.JSONDecodeError:
                configExists = False
    else:
        configExists = False

    userInput = gui.Dlg(title="DOORS Task Information")
    userInput.addField('Subject Number:', )
    # userInput.addField('Session:', 1)
    # userInput.addField('Version:', choices=[1, 2])
    userInput.addField('# of Practice Trials:', 5 if not configExists else loadedData['practiceTrials'])
    userInput.addField('# of TaskRun1:', choices=[49, 36])
    userInput.addField('# of TaskRun2:', choices=[49, 36])
    userInput.addField('Starting Distance', choices=[50, 'Random'])
    userInput.addField('Record Physiology', False if not configExists else loadedData['recordPhysio'])
    userInput.addField('Sensitivity (2: Less sensitive, 3: Normal, 4: More sensitive', 1 if not configExists else loadedData['sensitivity'] - 2, choices=[2, 3, 4])
    userInput.addField('Full Screen', True if not configExists else loadedData['fullScreen'])
    userInput.addField('Keyboard Mode', True if not configExists else loadedData['keyboardMode'])
    userInput.addField('Sound On?', True if not configExists else loadedData['soundOn'])
    userInput.addField('Save Data at Unexpected Quit', False if not configExists else loadedData['saveDataAtQuit'])
    userInput.addField('Save Config as Default', False if not configExists else loadedData['saveAsDefault'])
    # userInput.addField('Sound Mode:',choices=['PTB','Others'])
    return userInput.show()
