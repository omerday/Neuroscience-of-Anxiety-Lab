import os

from psychopy import gui
import json


def get_user_input(debug=False):
    """
    In charge of gathering initial info for configuration using gui.Dlg. it's being inserted into Params dictionary in
    the main file.
    :return: answer array
    """

    loaded_data = {}
    if os.path.exists("./data"):
        if os.path.exists("./data/FCconfig.json"):
            config_exists = True
            with open("./data/FCconfig.json") as file:
                try:
                    loaded_data = json.load(file)
                except json.decoder.JSONDecodeError:
                    config_exists = False
        else:
            config_exists = False
    else:
        os.mkdir("data")
        config_exists = False

    userInput = gui.Dlg(title="FC Task Configuration")
    userInput.addField('Subject Number:', )
    userInput.addField('Session:', 1)
    userInput.addField('Gender', "Female" if not config_exists else loaded_data["gender"], choices=["Male", "Female"])
    userInput.addField("Preferred Language", "Hebrew" if not config_exists else loaded_data["language"],
                       choices=["Hebrew", "English"])
    userInput.addField('Record Physiology', False if not config_exists else loaded_data['recordPhysio'])
    userInput.addField('Skip Instructions', False if not config_exists else loaded_data['skipInstructions'])
    userInput.addField('PreCond', False if not config_exists else loaded_data['preCond'])
    userInput.addField('Test', False if not config_exists else loaded_data['test'])
    userInput.addField('preCond New Version', False if not config_exists else loaded_data['preCondNewVersion'])
    userInput.addField('Test New Version', False if not config_exists else loaded_data['testNewVersion'])
    return userInput.show()
