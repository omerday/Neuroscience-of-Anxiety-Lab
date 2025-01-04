import os

from psychopy import gui
import json

TEMPS = ["34.0", "34.5", "35.0", "35.5", "36.0", "36.5", "37.0", "37.5", "38.0", "38.5", "39.0", "39.5", "40.0", "40.5",
         "41.0", "41.5",
         "42.0", "42.5", "43.0", "43.5", "44.0", "44.5", "45.0", "45.5", "46.0", "46.5", "47.0", "47.5", "48.0", "48.5",
         "49.0", "49.5", "50.0"]


def get_user_input(debug=False):
    """
    In charge of gathering initial info for configuration using gui.Dlg. it's being inserted into Params dictionary in
    the main file.
    :return: answer array
    """

    loaded_data = {}
    if os.path.exists("./data"):
        if os.path.exists("./data/TIMconfig.json"):
            config_exists = True
            with open("./data/TIMconfig.json") as file:
                try:
                    loaded_data = json.load(file)
                except json.decoder.JSONDecodeError:
                    config_exists = False
        else:
            config_exists = False
    else:
        os.mkdir("data")
        config_exists = False

    userInput = gui.Dlg(title="BlackTIM Task Configuration")
    userInput.addField('Subject Number:', )
    userInput.addField('Session:', 1)
    userInput.addField('Gender', "Female" if not config_exists else loaded_data["gender"], choices=["Male", "Female"])
    userInput.addField("Preferred Language", "Hebrew" if not config_exists else loaded_data["language"],
                       choices=["Hebrew", "English"])
    userInput.addField("fMRI Version", True if not config_exists else loaded_data["fmriVersion"])
    userInput.addField("T2", 0 if not config_exists else TEMPS.index(loaded_data['temps'][0]), choices=TEMPS)
    userInput.addField("T6", 0 if not config_exists else TEMPS.index(loaded_data['temps'][1]), choices=TEMPS)
    userInput.addField("Paradigm #", 1 if not config_exists else loaded_data["paradigm"] - 1, choices=[1, 2])
    userInput.addField("Pain Support", False if not config_exists else loaded_data["painSupport"])
    userInput.addField('Record Physiology', False if not config_exists else loaded_data['recordPhysio'])
    userInput.addField('Skip Instructions', False if not config_exists else loaded_data['skipInstructions'])
    userInput.addField('Continuous Shape', False if not config_exists else loaded_data['continuousShape'])
    userInput.addField("Don't Sleep After Temp", False)
    userInput.addField('More Ramp-Up Time', False)
    return userInput.show()
