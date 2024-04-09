import time
import datetime
import pygame
import pandas
import helpers
from psychopy import visual, core
import dataHandler

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


def beginning_vas(window: visual.Window, params, miniDf: pandas.DataFrame, summary_df: pandas.DataFrame, io):
    """
    The method presents the first set of VAS Questionnaire, destined to be shown at the beginning of the task.
    It shows each of the questions given in QUESTIONS_BEGINNING_MIDDLE_HE (or _EN given the language parameter)
    and the corresponding answers to be put as labels at each end of the scale.
    It returns only the Dataframes, with the answers updated.
    Args:
        window: visual.Window object
        params: parameters dictionary
        miniDf: mini dataframe
        summary_df:
        io: i/o component from the main code.

    Returns: three DataFrames with the answers updated

    """
    pygame.quit()
    for i in range(len(QUESTIONS_BEGINNING_MIDDLE_HE)):
        startTime = time.time()
        if params["language"] == "Hebrew":
            answer, dict_for_df = helpers.display_vas(window, params, QUESTIONS_BEGINNING_MIDDLE_HE[i],
                                               ANSWERS_BEGINNING_MIDDLE_HE[i], io=io, questionNo=i + 1, roundNo=1,)
        else:
            answer, dict_for_df = helpers.display_vas(window, params, QUESTIONS_BEGINNING_MIDDLE_EN[i],
                                                   ANSWERS_BEGINNING_MIDDLE_EN[i], io=io, questionNo=i + 1, roundNo=1,)
        dict_for_df['Section'] = "VAS1"
        dict_for_df['CurrentTime'] = round(time.time() - dict_for_df['StartTime'], 2)
        dict_for_df['VAS_score'] = answer
        dict_for_df['VAS_type'] = LABELS[i]
        dict_for_df['VAS_RT'] = time.time() - startTime

        miniDf = pandas.concat([miniDf, pandas.DataFrame.from_records([dict_for_df])])
        summary_df = pandas.concat([summary_df, pandas.DataFrame.from_records([dict_for_df])])

        dataHandler.save_backup(params, miniDF=miniDf, summary=summary_df)

    return miniDf, summary_df


def middle_vas(window: visual.Window, params, miniDf: pandas.DataFrame,
               summary_df: pandas.DataFrame, roundNum: int, io):
    """
        The method presents the next set of VAS Questionnaire, destined to be shown between different steps of the task.
        It shows each of the questions given in QUESTIONS_BEGINNING_MIDDLE_HE (or _EN given the language parameter)
        and the corresponding answers to be put as labels at each end of the scale.
        It returns only the Dataframes, with the answers updated.
        Args:
            window: visual.Window object
            params: parameters dictionary
            miniDf: mini dataframe
            summary_df:
            roundNum: number of session before-which the method was called
            io: i/o component from the main code.

        Returns: three DataFrames with the answers updated

        """
    pygame.quit()
    for i in range(len(QUESTIONS_BEGINNING_MIDDLE_HE)):
        startTime = time.time()
        if params["language"] == "Hebrew":
            answer, dict_for_df = helpers.display_vas(window, params, QUESTIONS_BEGINNING_MIDDLE_HE[i],
                                               ANSWERS_BEGINNING_MIDDLE_HE[i], questionNo=i + 1, io=io, roundNo=2)
        else:
            answer, dict_for_df = helpers.display_vas(window, params, QUESTIONS_BEGINNING_MIDDLE_EN[i],
                                                   ANSWERS_BEGINNING_MIDDLE_EN[i], questionNo=i + 1, io=io, roundNo=2)
        if roundNum == 2:
            dict_for_df['Section'] = "VAS2"
        elif roundNum == 3:
            dict_for_df['Section'] = "VAS3"
        else:
            dict_for_df['Section'] = "VASpost"
        dict_for_df['CurrentTime'] = round(time.time() - dict_for_df['StartTime'], 2)
        dict_for_df['VAS_score'] = answer
        dict_for_df['VAS_type'] = LABELS[i]
        dict_for_df['VAS_RT'] = time.time() - startTime

        miniDf = pandas.concat([miniDf, pandas.DataFrame.from_records([dict_for_df])])
        summary_df = pandas.concat([summary_df, pandas.DataFrame.from_records([dict_for_df])])

        dataHandler.save_backup(params, miniDF=miniDf, summary=summary_df)

    return miniDf, summary_df


def final_vas(window: visual.Window, params, miniDf: pandas.DataFrame, summary_df: pandas.DataFrame, io):
    """
        The method presents the last set of VAS Questionnaire, destined to be shown at the end of the experiment.
        It shows each of the questions given in QUESTIONS_FINAL_HE (or _EN given the language parameter)
        and the corresponding answers to be put as labels at each end of the scale.
        It returns only the Dataframes, with the answers updated.
        Args:
            window: visual.Window object
            params: parameters dictionary
            miniDf: mini dataframe
            summary_df:
            io: i/o component from the main code.

        Returns: three DataFrames with the answers updated

        """
    pygame.quit()
    for i in range(len(QUESTIONS_FINAL_HE)):
        startTime = time.time()
        if params["language"] == "Hebrew":
            answer, dict_for_df = helpers.display_vas(window, params, QUESTIONS_FINAL_HE[i], ANSWERS_FINAL_HE[i], io=io, questionNo=i + 1,
                                               roundNo=3)
        else:
            answer, dict_for_df = helpers.display_vas(window, params, QUESTIONS_FINAL_EN[i], ANSWERS_FINAL_EN[i], io=io,
                                                   questionNo=i + 1,
                                                   roundNo=3)
        dict_for_df["Section"] = 'Question'
        dict_for_df['CurrentTime'] = round(time.time() - dict_for_df['StartTime'], 2)
        dict_for_df['Q_type'] = QUESTIONS_LABEL[i]
        dict_for_df['Q_RT'] = time.time() - startTime
        dict_for_df['Q_score'] = answer

        miniDf = pandas.concat([miniDf, pandas.DataFrame.from_records([dict_for_df])])
        summary_df = pandas.concat([summary_df, pandas.DataFrame.from_records([dict_for_df])])

        dataHandler.save_backup(params, miniDF=miniDf, summary=summary_df)

    return miniDf, summary_df
