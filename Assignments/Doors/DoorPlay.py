import math
import random

import DoorPlayInfra
import helpers
from psychopy import visual, core


def practice_run():
    pass


def task_1(window: visual.Window, params: dict, roundNum: int, coinsNumber: int):
    # If round2, run show_middle_screen and VAS#2
    isKeyboard = params['keyboardMode']

    sizeOfArray = int(math.sqrt(params[f'numOfScreensTask{roundNum}']))
    scenariosList = helpers.get_p_r_couples(sizeOfArray)

    while len(scenariosList) != 0:
        scenario = random.choice(scenariosList)
        image, distanceFromDoor = DoorPlayInfra.setup_door(window, params, scenario[0], scenario[1])
        win, total_time = DoorPlayInfra.start_door(window, params, image, scenario[0], scenario[1], distanceFromDoor)
        coinsNumber += win
        scenariosList.remove(scenario)

