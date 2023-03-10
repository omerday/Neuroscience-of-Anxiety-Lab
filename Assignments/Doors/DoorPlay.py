import math
import random
import SetupDF
import pandas
import DoorPlayInfra
import helpers
import time
from psychopy import visual, core


def practice_run():
    pass


def run_task(window: visual.Window, params: dict, session: int, coinsNumber: int, Df: pandas.DataFrame):
    dict = SetupDF.create_dict_for_df(params, StepName='Doors', Session=session, TotalCoins=coinsNumber,)

    sizeOfArray = int(math.sqrt(params[f'numOfScreensTask{session}']))
    scenariosList = helpers.get_p_r_couples(sizeOfArray)

    roundNum = 0
    while len(scenariosList) != 0:
        roundNum = roundNum + 1
        scenario = random.choice(scenariosList)
        image, distanceFromDoor = DoorPlayInfra.setup_door(window, params, scenario[0], scenario[1])
        dict['RewardAmount'] = scenario[0]
        dict['PunishmentAmount'] = scenario[1]
        dict['Round'] = roundNum
        dict['StartTime'] = pandas.to_datetime(time.time())
        dict['DistanceAtStart'] = distanceFromDoor
        win, total_time = DoorPlayInfra.start_door(window, params, image, scenario[0], scenario[1], distanceFromDoor)
        coinsNumber += win
        scenariosList.remove(scenario)

    return Df
