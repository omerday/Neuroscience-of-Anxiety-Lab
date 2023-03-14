import math
import time
from psychopy import core, event, visual
from psychopy.visual import ratingscale
import SetupDF
import pandas
import datetime


def wait_for_space(window, Df: pandas.DataFrame, dict: dict):
    """
    Helper method to wait for a Spacebar keypress and keep the window open until the window
    :param dictForDf:
    :param Df:
    :param window:
    :return:
    """
    c = event.getKeys()
    while 'space' not in c and 'escape' not in c:
        dict['CurrentTime'] = datetime.datetime.now()
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        core.wait(1 / 1000)
        c = event.getKeys()
    if 'escape' in c:
        window.close()
        core.quit()
    return Df


def wait_for_space_with_replay(window, Df: pandas.DataFrame, dict: dict):
    """
    Helper method to wait for a Spacebar keypress and keep the window open until the window
    :param dictForDf:
    :param Df:
    :param window:
    :return:
    """
    c = event.getKeys()
    while 'space' not in c and 'escape' not in c and 'r' not in c:
        event.clearEvents()
        dict['CurrentTime'] = datetime.datetime.now()
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        core.wait(1 / 1000)
        c = event.getKeys()
    if 'escape' in c:
        window.close()
        core.quit()
    if 'r' in c:
        return Df, True
    return Df, False


def wait_for_space_no_df(window):
    """
    Helper method to wait for a Spacebar keypress and keep the window open until the window
    :param dictForDf:
    :param Df:
    :param window:
    :return:
    """
    core.wait(1 / 120)
    c = event.getKeys()
    while 'space' not in c and 'escape' not in c:
        core.wait(1 / 120)
        c = event.getKeys()
    if 'escape' in c:
        window.close()
        core.quit()


def wait_for_click(window):
    mouse = event.Mouse()
    mousePressed = mouse.getPressed()
    while mousePressed[0] != 1:
        mousePressed = mouse.getPressed()
    return


def display_vas(win, params, text, labels, Df: pandas.DataFrame, questionNo: int, roundNo: int):
    """
    A helper method that displays VAS question (text object) and places a scale using psychopy.visual.ratingscale.
    The scale goes between two labels, and the answer (1-10_ is saved to Df, along with the response time
    :param win:
    :param params:
    :param text:
    :param labels:
    :return:
    """
    # TODO: Set up a dictionary that contains data for DataFrame
    # TODO: Add a DataFrame and write the answers to it

    scale = ratingscale.RatingScale(win,
                                    labels=labels,  # Labels at the edges of the scale
                                    scale=None, choices=None, low=0, high=100, precision=1, tickHeight=0, size=2,
                                    textSize=0.6, acceptText='Continue', showValue=False, showAccept=True,
                                    markerColor="Yellow")
    textItem = visual.TextStim(win, text=text, height=.12, units='norm', pos=[0, 0.3], wrapWidth=2)

    dict = SetupDF.create_dict_for_df(params, StepName='VAS', VASQuestionNumber=questionNo, Session=roundNo)
    while scale.noResponse:
        dict['CurrentTime'] = datetime.datetime.now()
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        scale.draw()
        textItem.draw()
        win.flip()
        get_escape()
    return scale.getRating(), Df, dict


def get_escape():
    keys = event.getKeys()
    if keys == ['q'] or keys == ['Q'] or keys == ['Esc']:
        core.quit()


def get_p_r_couples(size: int):
    """
    the method returns a list with all the combos of p and r according to the size received from the user
    :param size:
    :return:
    """
    comboList = []
    for i in range(size):
        for j in range(size):
            comboList.append((i + 1, j + 1))
    return comboList


def display_image_for_time(window: visual.Window, params: dict, imagePath: str, timeframe: int, Df: pandas.DataFrame,
                           dictForDf: dict):
    image = visual.ImageStim(win=window, image=imagePath, units='pix', size=(params['screenSize'][0],
                                                                             params['screenSize'][1]),
                             opacity=1)
    image.draw()
    window.update()
    key = event.getKeys()
    endTime = time.time() + timeframe
    while time.time() < endTime and 'space' not in key:
        dictForDf['CurrentTime'] = datetime.datetime.now()
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        key = event.getKeys()
    return Df


def display_image_until_key(window: visual.Window, params: dict, imagePath: str, key: str, Df: pandas.DataFrame,
                            dictForDf: dict):
    image = visual.ImageStim(win=window, image=imagePath, units='pix', size=(params['screenSize'][0],
                                                                             params['screenSize'][1]),
                             opacity=1)
    image.draw()
    window.update()
    pressedKey = event.getKeys()
    while key not in pressedKey:
        dictForDf['CurrentTime'] = datetime.datetime.now()
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        pressedKey = event.getKeys()
    return Df
