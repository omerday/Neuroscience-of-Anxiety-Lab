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


def practice_run(window: visual.Window, params: dict, miniDf: pandas.DataFrame,
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
        coinsWon, total_time, miniDf, dict_for_df, lock = DoorPlayInfra.start_door(window, params, image, 0, 0, 0,
                                                                        distanceFromDoor, dict_for_df, io, 0, miniDf, summary_df,
                                                                        ser)

        # Add data to Df
        dict_for_df["CurrentTime"] = round(time.time() - dict_for_df['StartTime'], 2)
        summary_df = pandas.concat([summary_df, pandas.DataFrame.from_records([dict_for_df])])

        subtrial = subtrial + 1

    return miniDf, summary_df


def run_task(window: visual.Window, params: dict, blockNumber: int, totalCoins: int,
             miniDf: pandas.DataFrame, summary_df: pandas.DataFrame, io, ser=None):

    """
    Launch the entire doors task, with all 36/49 doors.
    Goes through an array of all the P&R combinations, and execute them one after another.
    Returns the dataframe with the collected data.
    If roundNum == 0 - that's a simulation run, and we should run just 5 doors (or however is given in the parameters)

    Args:
        window: visual.Window object
        params: parameters dictionary
        blockNumber: number of round executed
        totalCoins: amount of coins gathered so far
        miniDf:
        summary_df:
        io: i/o component from the main code
        ser: serial object for communication with BioPac. default is None.

    Returns: three dataframes, as well as the total coins after running the round.

    """
    if blockNumber not in [0, 1]:
        DoorPlayInfra.show_screen_pre_match(window, params, blockNumber, io, coins=totalCoins, mini_df=miniDf, summary_df=summary_df)

    if blockNumber in [1, 2]:
        helpers.show_version_specific_message(window, params, blockNumber, io)

    numOfDoors = 36 if params[f'numOfDoors'] == "36 (6x6)" else 49
    sizeOfArray = int(math.sqrt(numOfDoors))
    scenariosList = helpers.get_p_r_couples(sizeOfArray)

    if blockNumber == 0:
        for i in range(0, numOfDoors - params['numOfSimulationDoors']):
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

    screamDoors = []
    if params['screamVersion'] and blockNumber == params['ACTBlock']:
        screamDoors = [
            random.randint(5, 8),
            random.randint(13, 16),
            random.randint(28, 31)
        ]
    print(f"Scream was set for the following doors - {screamDoors}")

    while scenariosList or (params[f'numOfDoors'] == "36 (7x7)" and subtrial < 36):
        # Select a scenario and setup door
        subtrial += 1
        scenario = random.choice(scenariosList)
        scenarioIndex = (scenario[0] - 1) * 7 + (scenario[1]) + 50
        image, distanceFromDoor = DoorPlayInfra.setup_door(window, params, scenario[0], scenario[1])

        # Setup new dictionary
        dict_for_df = dataHandler.create_dict_for_df(params, Section=f'TaskRun{blockNumber}' if blockNumber != 0 else "Simulation", Round=blockNumber, TotalCoins=totalCoins, )
        dict_for_df['Reward_magnitude'] = scenario[0]
        dict_for_df['Punishment_magnitude'] = scenario[1]
        dict_for_df['Subtrial'] = subtrial
        dict_for_df['DistanceAtStart'] = distanceFromDoor * 100 if distanceFromDoor != 0 else 50
        dict_for_df["ScenarioIndex"] = scenarioIndex
        block_type = ""
        if blockNumber == params['ACTBlock']:
            block_type = "ACTIVE"
        elif blockNumber in [1, 2]:
            block_type = "NEUTRAL"
        dict_for_df["BlockType"] = block_type

        if params['recordPhysio']:
            serialHandler.report_event(ser, scenarioIndex)

        highValue = True if params["highValue"] and params["ACTBlock"] == blockNumber else False
        # Execute Door of selected scenario
        coinsWon, total_time, miniDf, dict_for_df, lock = DoorPlayInfra.start_door(window, params, image, scenario[0], scenario[1], totalCoins,
                                                                  distanceFromDoor, dict_for_df, io, scenarioIndex, miniDf, summary_df, ser, subtrial in screamDoors, highValue)
        totalCoins += coinsWon
        scenariosList.remove(scenario)

        # Add data to Df
        dict_for_df["Total_coins"] = totalCoins
        dict_for_df["CurrentTime"] = round(time.time() - dict_for_df['StartTime'], 2)

        dict_for_df["ScenarioIndex"] = scenarioIndex
        summary_df = pandas.concat([summary_df, pandas.DataFrame.from_records([dict_for_df])])

        dataHandler.save_backup(params, miniDF=miniDf, summary=summary_df)

    if blockNumber == 0:
        DoorPlayInfra.show_screen_post_simulation(window, params, io, miniDf)

    return miniDf, summary_df, totalCoins
