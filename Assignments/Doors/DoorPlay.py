import datetime
import math
import random
import dataHandler
import pandas
import DoorPlayInfra
import helpers
import time
import serial
from psychopy import visual, core


def practice_run(window: visual.Window, params: dict, Df: pandas.DataFrame, miniDf: pandas.DataFrame, io, ser=None):

    show_screen_pre_match(window, params, 0, io)

    roundNum = 1
    while roundNum <= 5:
        image, distanceFromDoor = DoorPlayInfra.setup_door(window, params, 0, 0)

        # Setup new dictionary
        dict = dataHandler.create_dict_for_df(params, StepName='Practice', )
        dict['RewardAmount'] = 0
        dict['PunishmentAmount'] = 0
        dict['Subtrial'] = roundNum
        dict['DistanceAtStart'] = distanceFromDoor * 100

        # Execute Door of selected scenario
        coinsWon, total_time, Df, dict, lock = DoorPlayInfra.start_door(window, params, image, 0, 0,
                                                                        distanceFromDoor, Df, dict, io, 0,
                                                                        ser)

        # Add data to Df
        dict["CurrentTime"] = round(time.time() - dict['StartTime'], 3)
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        miniDf = pandas.concat([miniDf, pandas.DataFrame.from_records([dict])])

        roundNum = roundNum + 1

    return Df, miniDf


def run_task(window: visual.Window, params: dict, session: int, totalCoins: int, Df: pandas.DataFrame,
             miniDf: pandas.DataFrame, io, ser=None):

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
    show_screen_pre_match(window, params, session, io, totalCoins)

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
        dict = dataHandler.create_dict_for_df(params, StepName='Doors', Session=session, TotalCoins=totalCoins, )
        dict['RewardAmount'] = scenario[0]
        dict['PunishmentAmount'] = scenario[1]
        dict['Subtrial'] = roundNum
        dict['DistanceAtStart'] = distanceFromDoor * 100

        # Execute Door of selected scenario
        coinsWon, total_time, Df, dict, lock = DoorPlayInfra.start_door(window, params, image, scenario[0], scenario[1],
                                                                  distanceFromDoor, Df, dict, io, scenarioIndex, ser)
        totalCoins += coinsWon
        scenariosList.remove(scenario)

        # Add data to Df
        dict["TotalCoins"] = totalCoins
        dict["CurrentTime"] = round(time.time() - dict['StartTime'], 3)
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        miniDf = pandas.concat([miniDf, pandas.DataFrame.from_records([dict])])

    return Df, miniDf


def show_screen_pre_match(window: visual.Window, params: dict, session: int, io, coins=0):
    if session == 2:
        if params["keyboardMode"]:
            message = visual.TextStim(window,
                                      text=f"Let’s rest for a bit. You have {coins} coins. Press Space when you "
                                           f"are ready to keep playing.", units="norm", color=(255, 255, 255))
        else:
            message = visual.TextStim(window, text=f"Let’s rest for a bit. You have {coins} coins. Click when you "
                                                   f"are ready to keep playing.", units="norm", color=(255, 255, 255))
        message.draw()

    else:
        screenNames = ["practice_start" ,"start_main_game"]
        image = visual.ImageStim(win=window, units="norm", opacity=1, size=(2, 2) if not params['fullScreen'] else None)
        image.image = "./img/instructions/" + screenNames[session] + ".jpg"
        image.draw()

    window.update()
    if params["keyboardMode"]:
        Df = helpers.wait_for_space_no_df(window, io)
    else:
        Df = helpers.wait_for_joystick_no_df(window)
