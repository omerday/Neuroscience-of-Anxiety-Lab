import time
import datetime
import pygame
import pandas
import helpers
from psychopy import visual, core

QUESTIONS_BEGINNING_MIDDLE = ["כמה אתם מרגישים לחוצים כרגע?",
                              "כמה אתם מעוניינים לקחת חלק במשימה?",
                              "כמה עייפים אתם כרגע?",
                              "חשבו על מצב הרוח שלכם כרגע. איך הייתם מתארים אותו?"]
ANSWERS_BEGINNING_MIDDLE = [["לא לחוץ", "מאוד לחוץ"], ["כלל לא", "במידה רבה"],
                            ["לא עייף כלל", "מאוד עייף"],
                            ["מצב רוח ירוד מאוד", "מצב רוח טוב מאוד"]]
QUESTIONS_FINAL = ["בכמה מטבעות זכית לדעתך?", "כמה מטבעות הפסדת לדעתך?", "באיזו תדירות ראית מפלצת כשהדלת נפתחה?",
                   "באיזו תדירות זכית במטבעות כשהדלת נפתחה?", "מה הרגשתך לגבי הביצועים שלך עד כה?"]
ANSWERS_FINAL = [["זכיתי במעט מאוד", "זכיתי בהמון"], ["הפסדתי מעט מאוד", "הפסדתי המון"], ["אף פעם", "כל הזמן"],
                 ["אף פעם", "כל הזמן"], ["עצוב, לא הצלחתי", "שמח, הצלחתי"]]


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
