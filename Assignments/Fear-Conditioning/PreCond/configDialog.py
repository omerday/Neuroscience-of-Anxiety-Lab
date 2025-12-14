import os

from psychopy import gui
import json
import helpers


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
    userInput.addField('Subject ID:', )
    userInput.addField('Session:', 1)
    userInput.addField('Gender', 0 if not config_exists else loaded_data["gender"], choices=["Male", "Female"])
    userInput.addField("Preferred Language", "Hebrew" if not config_exists else loaded_data["language"],
                       choices=["Hebrew", "English"])
    userInput.addField('Record Physiology', False if not config_exists else loaded_data['recordPhysio'])
    userInput.addField('Skip Instructions', False if not config_exists else loaded_data['skipInstructions'])
    userInput.addField('Phase', 0 if not config_exists else helpers.STEPS.index(loaded_data['phase']),
                       choices=helpers.STEPS)
    userInput.addField('Version', 0 if not config_exists else helpers.VERSION.index(loaded_data['version']),
                       choices=helpers.VERSION)
    userInput.addField('Combination',
                       0 if not config_exists else loaded_data['faceCombinationIndex'] - 1, choices=range(1, 7))
    userInput.addField('Cond. Sequence', 0 if not config_exists else loaded_data['conditioningSequenceIndex'] - 1, choices=range(1,3))
    return userInput.show()
