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

    """
    Launch the entire doors task, with all 36/49 doors.
    Goes through an array of all the P&R combinations, and execute them one after another.
    Returns the dataframe with the collected data.
    :param window:
    :param params:
    :param session:
    :param totalCoins:
    :param Df:
    :return:
    """

    sizeOfArray = int(math.sqrt(params[f'numOfScreensTask{session}']))
    scenariosList = helpers.get_p_r_couples(sizeOfArray)

    # Scenarios List indexing method:
    # (reward - 1) * 7 + Punishment - 1
    # For example:
    # Reward 1 Punishment 1 - index 0
    # Reward 5 Punishment 2 - index 29

    roundNum = 0
    while len(scenariosList) != 0:

        # Select a scenario and setup door
        roundNum = roundNum + 1
        scenario = random.choice(scenariosList)
        scenarioIndex = (scenario[0] - 1) * 7 + (scenario[1] - 1)
        image, distanceFromDoor = DoorPlayInfra.setup_door(window, params, scenario[0], scenario[1])

        # Setup new dictionary
        dict = SetupDF.create_dict_for_df(params, StepName='Doors', Session=session, TotalCoins=totalCoins, )
        dict['RewardAmount'] = scenario[0]
        dict['PunishmentAmount'] = scenario[1]
        dict['Round'] = roundNum
        dict['DistanceAtStart'] = distanceFromDoor

        # Execute Door of selected scenario
        coinsWon, total_time, Df, dict = DoorPlayInfra.start_door(window, params, image, scenario[0], scenario[1], distanceFromDoor, Df, dict)
        totalCoins += coinsWon
        scenariosList.remove(scenario)

        # Add data to Df
        dict["TotalCoins"] = totalCoins
        dict["CurrentTime"] = round(time.time() - dict['StartTime'], 3)
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        Df.to_csv('./Df.csv')

    return Df
