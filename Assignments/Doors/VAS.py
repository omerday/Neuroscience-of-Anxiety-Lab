import time
import datetime
import pygame
import pandas
import helpers
from psychopy import visual, core

QUESTIONS_BEGINNING_MIDDLE = ["How anxious do you feel right now?",
                              "How much do you feel like taking part in the task?",
                              "How tired are you right now?",
                              "Think about your mood right now. How would you describe it?"]
ANSWERS_BEGINNING_MIDDLE = [["Not anxious", "Very anxious"], ["Not at all", "Very much"],
                            ["Not tired at all", "Very tired"],
                            ["Worst mood possible", "Best mood possible"]]
QUESTIONS_FINAL = ["How many coins do you think you won?", "How many coins do you think you lost?", "How often did "
                                                                                                    "you see the "
                                                                                                    "monster when the "
                                                                                                    "door opened?",
                   "How often did you win coins when the door opened?", "How do you feel about how well you’ve done "
                                                                        "so far?"]
ANSWERS_FINAL = [["Won very few", "Won very many"], ["Lost very few", "Lost very many"], ["never", "all the time"],
                 ["never", "all the time"], ["sad, I did badly", "happy, I did great"]]


def beginning_vas(window: visual.Window, params, Df: pandas.DataFrame, miniDf: pandas.DataFrame):
    pygame.quit()
    window.mouseVisible = True
    for i in range(len(QUESTIONS_BEGINNING_MIDDLE)):
        startTime = time.time()
        answer, Df, dict = helpers.display_vas(window, params, QUESTIONS_BEGINNING_MIDDLE[i],
                                               ANSWERS_BEGINNING_MIDDLE[i], Df, questionNo=i + 1, roundNo=1)

        dict['CurrentTime'] = round(time.time() - dict['StartTime'], 3)
        dict['VASAnswer'] = answer
        dict['VAS_RT'] = time.time() - startTime
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        miniDf = pandas.concat([miniDf, pandas.DataFrame.from_records([dict])])
    window.mouseVisible = False
    return Df, miniDf


def middle_vas(window: visual.Window, params, Df: pandas.DataFrame, miniDf: pandas.DataFrame):
    window.mouseVisible = True
    for i in range(len(QUESTIONS_BEGINNING_MIDDLE)):
        startTime = time.time()
        answer, Df, dict = helpers.display_vas(window, params, QUESTIONS_BEGINNING_MIDDLE[i],
                                               ANSWERS_BEGINNING_MIDDLE[i], Df, questionNo=i + 1, roundNo=2)
        dict['CurrentTime'] = round(time.time() - dict['StartTime'], 3)
        dict['VASAnswer'] = answer
        dict['VAS_RT'] = time.time() - startTime
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        miniDf = pandas.concat([miniDf, pandas.DataFrame.from_records([dict])])

    window.mouseVisible = False
    return Df, miniDf


def final_vas(window: visual.Window, params, Df: pandas.DataFrame, miniDf: pandas.DataFrame):
    window.mouseVisible = True
    for i in range(len(QUESTIONS_FINAL)):
        startTime = time.time()
        answer, Df, dict = helpers.display_vas(window, params, QUESTIONS_FINAL[i], ANSWERS_FINAL[i], Df, questionNo=i + 1,
                                               roundNo=3)
        dict['CurrentTime'] = round(time.time() - dict['StartTime'], 3)
        dict['VAS_RT'] = time.time() - startTime
        dict['VASAnswer'] = answer
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        miniDf = pandas.concat([miniDf, pandas.DataFrame.from_records([dict])])

    window.mouseVisible = False
    return Df, miniDf
