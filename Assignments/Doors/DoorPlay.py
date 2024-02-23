import datetime
import math
import random

import psychopy.visual
import pygame
import serialHandler
import dataHandler
import pandas
import DoorPlayInfra
import helpers
import time
import serial
from psychopy import visual, core


def practice_run(window: visual.Window, params: dict, full_df: pandas.DataFrame, mini_df: pandas.DataFrame,
                 summary_df: pandas.DataFrame, io, ser=None, practice_trials=0):

    # DoorPlayInfra.show_screen_pre_match(window, params, 0, io, df=Df, mini_df=miniDf, summary_df=summary_df)

    subtrial = 1
    if practice_trials == 0:
        practice_trials = params['practiceTrials']
    while subtrial <= practice_trials:
        image, distanceFromDoor = DoorPlayInfra.setup_door(window, params, 0, 0)

        # Setup new dictionary
        dict_for_df = dataHandler.create_dict_for_df(params, Section='Practice', )
        dict_for_df['Reward_magnitude'] = 0
        dict_for_df['Punishment_magnitude'] = 0
        dict_for_df['Subtrial'] = subtrial
        dict_for_df['DistanceAtStart'] = distanceFromDoor * 100

        # Execute Door of selected scenario
        coinsWon, total_time, full_df, mini_df, dict_for_df, lock = DoorPlayInfra.start_door(window, params, image, 0, 0, 0,
                                                                                             distanceFromDoor, full_df, dict_for_df, io, 0, mini_df, summary_df,
                                                                                             ser)

        # Add data to Df
        dict_for_df["CurrentTime"] = round(time.time() - dict_for_df['StartTime'], 2)
        if params['saveFullDF']:
            full_df = pandas.concat([full_df, pandas.DataFrame.from_records([dict_for_df])])
        summary_df = pandas.concat([summary_df, pandas.DataFrame.from_records([dict_for_df])])

        subtrial = subtrial + 1

    return full_df, mini_df, summary_df


def run_task(window: visual.Window, params: dict, roundNum: int, totalCoins: int, full_df: pandas.DataFrame,
             mini_df: pandas.DataFrame, summary_df: pandas.DataFrame, io, ser=None, simulation=False):

    """
    Launch the entire doors task, with all 36/49 doors.
    Goes through an array of all the P&R combinations, and execute them one after another.
    Returns the dataframe with the collected data.
    If roundNum == 0 - that's a simulation run, and we should run just 10 doors
    :param window:
    :param params:
    :param round:
    :param totalCoins:
    :param full_df:
    :return:
    """
    if roundNum not in [0, 1]:
        DoorPlayInfra.show_screen_pre_match(window, params, roundNum, io, coins=totalCoins, df=full_df, mini_df=mini_df, summary_df=summary_df)

    sizeOfArray = int(math.sqrt(params[f'numOfDoors']))
    scenariosList = helpers.get_p_r_couples(sizeOfArray)

    if roundNum == 0:
        for i in range(0, params[f'numOfDoors'] - params['numOfSimulationDoors']):
            scenariosList.remove(random.choice(scenariosList))
        print(scenariosList)
    # Scenarios List indexing method:
    # (reward - 1) * 7 + Punishment
    # For example:
    # Reward 1 Punishment 1 - index 1
    # Reward 5 Punishment 2 - index 30

    # When sending a signal to biopac, we'll add 1 to the scenario in order to avoid 0 from being sent.
    # This should be deduced from the event channel when analyzing the .acq file.

    subtrial = 0
    while scenariosList:

        # Select a scenario and setup door
        subtrial = subtrial + 1
        scenario = random.choice(scenariosList)
        scenarioIndex = (scenario[0] - 1) * 7 + (scenario[1]) + 50
        image, distanceFromDoor = DoorPlayInfra.setup_door(window, params, scenario[0], scenario[1])

        # Setup new dictionary
        dict_for_df = dataHandler.create_dict_for_df(params, Section=f'TaskRun{roundNum}' if roundNum != 0 else "Simulation", Round=roundNum, TotalCoins=totalCoins, )
        dict_for_df['Reward_magnitude'] = scenario[0]
        dict_for_df['Punishment_magnitude'] = scenario[1]
        dict_for_df['Subtrial'] = subtrial
        dict_for_df['DistanceAtStart'] = distanceFromDoor * 100 if distanceFromDoor != 0 else 50

        if params['recordPhysio'] and not simulation:
            dict_for_df["ScenarioIndex"] = scenarioIndex
            serialHandler.report_event(ser, scenarioIndex)

        # Execute Door of selected scenario
        coinsWon, total_time, full_df, mini_df, dict_for_df, lock = DoorPlayInfra.start_door(window, params, image, scenario[0], scenario[1], totalCoins,
                                                                                             distanceFromDoor, full_df, dict_for_df, io, scenarioIndex, mini_df, summary_df, ser, simulation)
        totalCoins += coinsWon
        scenariosList.remove(scenario)

        # Add data to Df
        dict_for_df["Total_coins"] = totalCoins
        dict_for_df["CurrentTime"] = round(time.time() - dict_for_df['StartTime'], 2)

        if params['saveFullDF']:
            full_df = pandas.concat([full_df, pandas.DataFrame.from_records([dict_for_df])])
        if not simulation:
            dict_for_df["ScenarioIndex"] = scenarioIndex
        summary_df = pandas.concat([summary_df, pandas.DataFrame.from_records([dict_for_df])])

        dataHandler.save_backup(params, fullDF=full_df, miniDF=mini_df, summary=summary_df)

    if roundNum == 0:
        DoorPlayInfra.show_screen_post_simulation(window, params, io, full_df, mini_df)

    return full_df, mini_df, summary_df, totalCoins
