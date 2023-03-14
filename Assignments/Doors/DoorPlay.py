import datetime
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


def run_task(window: visual.Window, params: dict, session: int, totalCoins: int, Df: pandas.DataFrame):

    sizeOfArray = int(math.sqrt(params[f'numOfScreensTask{session}']))
    scenariosList = helpers.get_p_r_couples(sizeOfArray)

    roundNum = 0
    while len(scenariosList) != 0:
        dict = SetupDF.create_dict_for_df(params, StepName='Doors', Session=session, TotalCoins=totalCoins, )
        roundNum = roundNum + 1
        scenario = random.choice(scenariosList)
        image, distanceFromDoor = DoorPlayInfra.setup_door(window, params, scenario[0], scenario[1])
        dict['RewardAmount'] = scenario[0]
        dict['PunishmentAmount'] = scenario[1]
        dict['Round'] = roundNum
        dict['DistanceAtStart'] = distanceFromDoor
        coinsWon, total_time, Df, dict = DoorPlayInfra.start_door(window, params, image, scenario[0], scenario[1], distanceFromDoor, Df, dict)
        totalCoins += coinsWon
        scenariosList.remove(scenario)
        dict["TotalCoins"] = totalCoins
        dict["CurrentTime"] = round(time.time() - dict['StartTime'], 3)
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])

    return Df
