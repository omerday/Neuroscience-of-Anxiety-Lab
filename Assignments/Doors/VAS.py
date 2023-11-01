import time
import datetime
import pygame
import pandas
import helpers
from psychopy import visual, core

LABELS = ["Anxiety", "Avoidance", "Tired", "Mood"]
QUESTIONS_BEGINNING_MIDDLE_HE = ["כמה אתם מרגישים לחוצים כרגע?",
                              "כמה אתם מעוניינים לקחת חלק במשימה?",
                              "כמה עייפים אתם כרגע?",
                              "חשבו על מצב הרוח שלכם כרגע. איך הייתם מתארים אותו?"]
QUESTIONS_BEGINNING_MIDDLE_EN = ["How anxious do you feel right now?",
                              "How much do you feel like taking part in the task?",
                              "How tired are you right now?",
                              "Think about your mood right now. How would you describe it?"]

ANSWERS_BEGINNING_MIDDLE_HE = [["לא לחוץ", "מאוד לחוץ"], ["כלל לא", "במידה רבה"],
                               ["לא עייף כלל", "מאוד עייף"],
                               ["מצב רוח ירוד מאוד", "מצב רוח טוב מאוד"]]
ANSWERS_BEGINNING_MIDDLE_EN = [["Not anxious", "Very anxious"], ["Not at all", "Very much"],
                            ["Not tired at all", "Very tired"],
                            ["Worst mood possible", "Best mood possible"]]


QUESTIONS_LABEL = ["Won", "Lost", "Monster", "Coins", "Performance"]

QUESTIONS_FINAL_HE = ["בכמה מטבעות זכית לדעתך?", "כמה מטבעות הפסדת לדעתך?", "באיזו תדירות ראית מפלצת כשהדלת נפתחה?",
                   "באיזו תדירות זכית במטבעות כשהדלת נפתחה?", "מה הרגשתך לגבי הביצועים שלך עד כה?"]
QUESTIONS_FINAL_EN = ["How many coins do you think you won?", "How many coins do you think you lost?", "How often did "
                                                                                                    "you see the "
                                                                                                    "monster when the "
                                                                                                    "door opened?",
                   "How often did you win coins when the door opened?", "How do you feel about how well you’ve done "
                                                                        "so far?"]

ANSWERS_FINAL_HE = [["זכיתי במעט מאוד", "זכיתי בהמון"], ["הפסדתי מעט מאוד", "הפסדתי המון"], ["אף פעם", "כל הזמן"],
                    ["אף פעם", "כל הזמן"], ["עצוב, לא הצלחתי", "שמח, הצלחתי"]]
ANSWERS_FINAL_EN = [["Won very few", "Won very many"], ["Lost very few", "Lost very many"], ["never", "all the time"],
                 ["never", "all the time"], ["sad, I did badly", "happy, I did great"]]


def beginning_vas(window: visual.Window, params, Df: pandas.DataFrame, miniDf: pandas.DataFrame):
    pygame.quit()
    window.mouseVisible = True
    for i in range(len(QUESTIONS_BEGINNING_MIDDLE_HE)):
        startTime = time.time()
        if params["language"] == "Hebrew":
            answer, Df, dict = helpers.display_vas(window, params, QUESTIONS_BEGINNING_MIDDLE_HE[i],
                                               ANSWERS_BEGINNING_MIDDLE_HE[i], Df, questionNo=i + 1, roundNo=1)
        else:
            answer, Df, dict = helpers.display_vas(window, params, QUESTIONS_BEGINNING_MIDDLE_EN[i],
                                                   ANSWERS_BEGINNING_MIDDLE_EN[i], Df, questionNo=i + 1, roundNo=1)
        dict['Section'] = "VASpre"
        dict['CurrentTime'] = round(time.time() - dict['StartTime'], 3)
        dict['VAS_score'] = answer
        dict['VAS_type'] = LABELS[i]
        dict['VAS_RT'] = time.time() - startTime
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        miniDf = pandas.concat([miniDf, pandas.DataFrame.from_records([dict])])
    window.mouseVisible = False
    return Df, miniDf


def middle_vas(window: visual.Window, params, Df: pandas.DataFrame, miniDf: pandas.DataFrame, roundNum: int):
    window.mouseVisible = True
    for i in range(len(QUESTIONS_BEGINNING_MIDDLE_HE)):
        startTime = time.time()
        if params["language"] == "Hebrew":
            answer, Df, dict = helpers.display_vas(window, params, QUESTIONS_BEGINNING_MIDDLE_HE[i],
                                               ANSWERS_BEGINNING_MIDDLE_HE[i], Df, questionNo=i + 1, roundNo=2)
        else:
            answer, Df, dict = helpers.display_vas(window, params, QUESTIONS_BEGINNING_MIDDLE_EN[i],
                                                   ANSWERS_BEGINNING_MIDDLE_EN[i], Df, questionNo=i + 1, roundNo=2)
        if roundNum == 2:
            dict['Section'] = "VAS1"
        elif roundNum == 3:
            dict['Section'] = "VAS2"
        else:
            dict['Section'] = "VAS3"
        dict['CurrentTime'] = round(time.time() - dict['StartTime'], 3)
        dict['VAS_score'] = answer
        dict['VAS_type'] = LABELS[i]
        dict['VAS_RT'] = time.time() - startTime
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        miniDf = pandas.concat([miniDf, pandas.DataFrame.from_records([dict])])

    window.mouseVisible = False
    return Df, miniDf


def final_vas(window: visual.Window, params, Df: pandas.DataFrame, miniDf: pandas.DataFrame):
    window.mouseVisible = True
    for i in range(len(QUESTIONS_FINAL_HE)):
        startTime = time.time()
        if params["language"] == "Hebrew":
            answer, Df, dict = helpers.display_vas(window, params, QUESTIONS_FINAL_HE[i], ANSWERS_FINAL_HE[i], Df, questionNo=i + 1,
                                               roundNo=3)
        else:
            answer, Df, dict = helpers.display_vas(window, params, QUESTIONS_FINAL_EN[i], ANSWERS_FINAL_EN[i], Df,
                                                   questionNo=i + 1,
                                                   roundNo=3)
        dict["Section"] = 'Question'
        dict['CurrentTime'] = round(time.time() - dict['StartTime'], 3)
        dict['Q_type'] = QUESTIONS_LABEL[i]
        dict['Q_RT'] = time.time() - startTime
        dict['Q_score'] = answer
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        miniDf = pandas.concat([miniDf, pandas.DataFrame.from_records([dict])])

    window.mouseVisible = False
    return Df, miniDf
