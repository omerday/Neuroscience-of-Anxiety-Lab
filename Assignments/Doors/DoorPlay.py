import datetime
import math
import random

import psychopy.visual
import pygame

import dataHandler
import pandas
import DoorPlayInfra
import helpers
import time
import serial
from psychopy import visual, core


def practice_run(window: visual.Window, params: dict, Df: pandas.DataFrame, miniDf: pandas.DataFrame, io, ser=None):

    DoorPlayInfra.show_screen_pre_match(window, params, 0, io)

    subtrial = 1
    while subtrial <= params['practiceTrials']:
        image, distanceFromDoor = DoorPlayInfra.setup_door(window, params, 0, 0)

        # Setup new dictionary
        dict = dataHandler.create_dict_for_df(params, Section='Practice', )
        dict['RewardAmount'] = 0
        dict['PunishmentAmount'] = 0
        dict['Subtrial'] = subtrial
        dict['DistanceAtStart'] = distanceFromDoor * 100

        # Execute Door of selected scenario
        coinsWon, total_time, Df, dict, lock = DoorPlayInfra.start_door(window, params, image, 0, 0,
                                                                        distanceFromDoor, Df, dict, io, 0, miniDf,
                                                                        ser)

        # Add data to Df
        dict["CurrentTime"] = round(time.time() - dict['StartTime'], 3)
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        miniDf = pandas.concat([miniDf, pandas.DataFrame.from_records([dict])])

        subtrial = subtrial + 1

    return Df, miniDf


def run_task(window: visual.Window, params: dict, round: int, totalCoins: int, Df: pandas.DataFrame,
             miniDf: pandas.DataFrame, io, ser=None):

    """
    Launch the entire doors task, with all 36/49 doors.
    Goes through an array of all the P&R combinations, and execute them one after another.
    Returns the dataframe with the collected data.
    :param window:
    :param params:
    :param round:
    :param totalCoins:
    :param Df:
    :return:
    """
    DoorPlayInfra.show_screen_pre_match(window, params, round, io, totalCoins)

    sizeOfArray = int(math.sqrt(params[f'numOfDoors']))
    scenariosList = helpers.get_p_r_couples(sizeOfArray)

    # Scenarios List indexing method:
    # (reward - 1) * 7 + Punishment - 1
    # For example:
    # Reward 1 Punishment 1 - index 0
    # Reward 5 Punishment 2 - index 29

    subtrial = 0
    while len(scenariosList) != 0:

        # Select a scenario and setup door
        subtrial = subtrial + 1
        scenario = random.choice(scenariosList)
        scenarioIndex = (scenario[0] - 1) * 7 + (scenario[1] - 1)
        image, distanceFromDoor = DoorPlayInfra.setup_door(window, params, scenario[0], scenario[1])

        # Setup new dictionary
        dict = dataHandler.create_dict_for_df(params, Section=f'TaskRun{round}', Round=round, TotalCoins=totalCoins, )
        dict['RewardAmount'] = scenario[0]
        dict['PunishmentAmount'] = scenario[1]
        dict['Subtrial'] = subtrial
        dict['DistanceAtStart'] = distanceFromDoor * 100

        # Execute Door of selected scenario
        coinsWon, total_time, Df, dict, lock = DoorPlayInfra.start_door(window, params, image, scenario[0], scenario[1],
                                                                  distanceFromDoor, Df, dict, io, scenarioIndex, miniDf, ser)
        totalCoins += coinsWon
        scenariosList.remove(scenario)

        # Add data to Df
        dict["TotalCoins"] = totalCoins
        dict["CurrentTime"] = round(time.time() - dict['StartTime'], 3)
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        miniDf = pandas.concat([miniDf, pandas.DataFrame.from_records([dict])])

    return Df, miniDf, totalCoins
