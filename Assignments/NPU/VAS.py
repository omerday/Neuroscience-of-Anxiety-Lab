import time
import datetime
import pygame
import pandas
import helpers
from psychopy import visual, core
from psychopy.iohub import launchHubServer
from psychopy.iohub.client.keyboard import Keyboard
from psychopy.visual import ratingscale
import dataHandler

LABELS = ["Anxiety", "Avoidance", "Tired", "Mood"]
QUESTIONS_BEGINNING_MIDDLE_HE = ["כמה אתם מרגישים לחוצים כרגע?",
                              "כמה אתם מעוניינים לקחת חלק במשימה?",
                              "כמה עייפים אתם כרגע?",
                              "חשבו על מצב הרוח שלכם כרגע. איך הייתם מתארים אותו?"]
QUESTIONS_BEGINNING_MIDDLE_EN = ["How anxious do you feel right now?",
                              "How much do you feel like taking part in the task?",
                              "How tired are you right now?",
                              "Think about your mood right now.\nHow would you describe it?"]

ANSWERS_BEGINNING_MIDDLE_HE = [["לא לחוץ", "מאוד לחוץ"], ["כלל לא", "במידה רבה"],
                               ["לא עייף כלל", "מאוד עייף"],
                               ["מצב רוח ירוד מאוד", "מצב רוח טוב מאוד"]]
ANSWERS_BEGINNING_MIDDLE_EN = [["Not anxious", "Very anxious"], ["Not at all", "Very much"],
                            ["Not tired at all", "Very tired"],
                            ["Worst mood possible", "Best mood possible"]]


def vas(window: visual.Window, params, Df: pandas.DataFrame, miniDf: pandas.DataFrame, io, roundNum: int):
    pygame.quit()
    window.mouseVisible = True
    for i in range(len(QUESTIONS_BEGINNING_MIDDLE_HE)):
        startTime = time.time()
        if params["language"] == "Hebrew":
            answer, Df, dict_for_df = display_vas(window, params, QUESTIONS_BEGINNING_MIDDLE_HE[i],
                                               ANSWERS_BEGINNING_MIDDLE_HE[i], Df, io, questionNo=i + 1, roundNum=1)
        else:
            answer, Df, dict_for_df = display_vas(window, params, QUESTIONS_BEGINNING_MIDDLE_EN[i],
                                                   ANSWERS_BEGINNING_MIDDLE_EN[i], Df, io, questionNo=i + 1, roundNum=1)
        dict_for_df['Section'] = f"VAS{roundNum}"
        dict_for_df['CurrentTime'] = round(time.time() - dict_for_df['StartTime'], 2)
        dict_for_df['VAS_score'] = answer
        dict_for_df['VAS_type'] = LABELS[i]
        dict_for_df['VAS_RT'] = time.time() - startTime
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict_for_df])])
        miniDf = pandas.concat([miniDf, pandas.DataFrame.from_records([dict_for_df])])
    window.mouseVisible = False
    return Df, miniDf


def display_vas(window: visual.Window, params:dict, text, labels, Df: pandas.DataFrame, io, questionNo: int, roundNum: int):
    """
    A helper method that displays VAS question (text object) and places a scale using psychopy.visual.ratingscale.
    The scale goes between two labels, and the answer (1-100) is saved to Df, along with the response time
    :param roundNo:
    :param questionNo:
    :param Df:
    :param win:
    :param params:
    :param text:
    :param labels:
    :return: The VAS rating, along with the Dataframe and dict
    """
    keyboard = io.devices.keyboard
    if params["language"] == "Hebrew":
        scale = ratingscale.RatingScale(window,
                                        labels=[labels[0][::-1], labels[1][::-1]],  # Labels at the edges of the scale
                                        scale=None, choices=None, low=0, high=100, precision=1, tickHeight=0, size=2,
                                        textSize=0.6, acceptText='Continue', showValue=False, showAccept=True,
                                        markerColor="Maroon", acceptKeys=["space"], textColor="Black", lineColor="Black")
        textItem = visual.TextStim(window, text=text, height=.12, units='norm', pos=[0, 0.3], wrapWidth=2,
                                   languageStyle='RTL', font="Open Sans", color="Black")

    else:
        scale = ratingscale.RatingScale(window,
                                        labels=[labels[0], labels[1]],  # Labels at the edges of the scale
                                        scale=None, choices=None, low=0, high=100, precision=1, tickHeight=0, size=2,
                                        textSize=0.6, acceptText='Continue', showValue=False, showAccept=True,
                                        markerColor="Maroon", acceptKeys=["space"], textColor="Black", lineColor="Black")
        textItem = visual.TextStim(window, text=text, height=.12, units='norm', pos=[0, 0.3], wrapWidth=2,
                                   languageStyle="LTR", font="Open Sans", color="Black")

    dict_for_df = dataHandler.create_dict_for_df(params, Section='VAS', VASQuestionNumber=questionNo, Round=roundNum)
    while scale.noResponse:
        dict_for_df['CurrentTime'] = round(time.time() - dict_for_df['StartTime'], 2)
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict_for_df])])
        scale.draw()
        textItem.draw()
        window.flip()
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == "escape":
                window.close()
                core.quit()
    return scale.getRating(), Df, dict_for_df