import time
import pygame
from psychopy import core, event, visual
from psychopy.iohub import launchHubServer
from psychopy.iohub.client.keyboard import Keyboard
from psychopy.visual import ratingscale
import SetupDF
import pandas
import datetime


def wait_for_space(window, Df: pandas.DataFrame, dict: dict, io):
    """
    Helper method to wait for a Spacebar keypress and keep the window open until then
    :param dict:
    :param Df:
    :param window:
    :return:
    """
    keyboard = io.devices.keyboard
    while True:
        dict['CurrentTime'] = round(time.time() - dict['StartTime'], 3)
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == " ":
                return Df
            if event.key == "escape":
                window.close()
                core.quit()
                return Df

    # c = event.getKeys()
    # while 'space' not in c and 'escape' not in c:
    #     dict['CurrentTime'] = round(time.time() - dict['StartTime'], 3)
    #     Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
    #     core.wait(1 / 1000)
    #     c = event.getKeys()
    # if 'escape' in c:
    #     window.close()
    #     core.quit()
    # return Df


# TODO: Add Quit Button
def wait_for_joystick_press(window, Df: pandas.DataFrame, dict: dict):
    pygame.init()

    while True:
        dict['CurrentTime'] = round(time.time() - dict['StartTime'], 3)
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        core.wait(1 / 1000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.close()
                core.quit()
                break
            if event.type == pygame.JOYBUTTONDOWN:
                while True:
                    for currEvent in pygame.event.get():
                        if currEvent.type == pygame.JOYBUTTONUP:
                            return Df


# TODO: Replay doesnt work :(
def wait_for_space_with_replay(window, Df: pandas.DataFrame, dict: dict, io):
    """
    Helper method to wait for a Spacebar keypress and keep the window open, or get 'r' keypress for replay of the
     instructions. Returns True if needed to replay.
    :param dict:
    :param Df:
    :param window:
    :return: True/False if r was pressed
    """
    keyboard = io.devices.keyboard
    while True:
        dict['CurrentTime'] = round(time.time() - dict['StartTime'], 3)
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        keys = keyboard.getKeys()
        for event in keys:
            if event.key == 'r' or event.key == 'R':
                return Df, True
            if event.key == ' ':
                return Df, False
            if event.key == "escape":
                window.close()
                core.quit()


# TODO: Set a key for replay
# TODO: Set a key for quitting
def wait_for_joystick_press_with_replay(window, Df: pandas.DataFrame, dict: dict):
    """
    Helper method to wait for a joystick keypress and keep the window open, or get 'r' keypress for replay of the
     instructions. Returns True if needed to replay.
    :param dict:
    :param Df:
    :param window:
    :return: True/False if r was pressed
    """
    pygame.init()
    while True:
        dict['CurrentTime'] = round(time.time() - dict['StartTime'], 3)
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        core.wait(1 / 1000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.close()
                core.quit()
            if event.type == pygame.JOYBUTTONDOWN:
                while True:
                    for currEvent in pygame.event.get():
                        if currEvent.type == pygame.JOYBUTTONUP:
                            return Df, False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                while True:
                    for currEvent in pygame.event.get():
                        if currEvent.type == pygame.KEYUP and currEvent.key == pygame.K_r:
                            return Df, True


# TODO: Duplicate for joystick
def wait_for_space_no_df(window, io):
    """
    Helper method to wait for a Spacebar keypress and keep the window open, without writing to Df.
    :param window:
    :return:
    """

    keyboard = io.devices.keyboard
    while True:
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == " ":
                return
            if event.key == "escape":
                window.close()
                core.quit()

    # pygame.init()
    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             window.close()
    #             core.quit()
    #         if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
    #             while True:
    #                 for currEvent in pygame.event.get():
    #                     if currEvent.type == pygame.KEYUP and currEvent.key == pygame.K_SPACE:
    #                         return
    #         if event.type == pygame.JOYBUTTONDOWN:
    #             while True:
    #                 for currEvent in pygame.event.get():
    #                     if currEvent.type == pygame.JOYBUTTONUP:
    #                         return


def wait_for_click(window):
    mouse = event.Mouse()
    mousePressed = mouse.getPressed()
    while mousePressed[0] != 1:
        mousePressed = mouse.getPressed()
    return


def display_vas(win, params, text, labels, Df: pandas.DataFrame, questionNo: int, roundNo: int):
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

    scale = ratingscale.RatingScale(win,
                                    labels=labels,  # Labels at the edges of the scale
                                    scale=None, choices=None, low=0, high=100, precision=1, tickHeight=0, size=2,
                                    textSize=0.6, acceptText='Continue', showValue=False, showAccept=True,
                                    markerColor="Yellow")
    textItem = visual.TextStim(win, text=text, height=.12, units='norm', pos=[0, 0.3], wrapWidth=2)

    dict = SetupDF.create_dict_for_df(params, StepName='VAS', VASQuestionNumber=questionNo, Session=roundNo)
    while scale.noResponse:
        # dict['CurrentTime'] = datetime.datetime.now() - dict['StartTime']
        dict['CurrentTime'] = round(time.time() - dict['StartTime'], 3)
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
        dictForDf['CurrentTime'] = round(time.time() - dictForDf['StartTime'], 3)
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
        dictForDf['CurrentTime'] = round(time.time() - dictForDf['StartTime'], 3)
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        pressedKey = event.getKeys()
    return Df
