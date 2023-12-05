import time
import pygame
from psychopy import core, event, visual
from psychopy.iohub import launchHubServer
from psychopy.iohub.client.keyboard import Keyboard
from psychopy.visual import ratingscale
import dataHandler
import pandas
import datetime


def wait_for_space(window, Df: pandas.DataFrame, dict_for_df: dict, io, params=None, mini_df=None):
    """
    Helper method to wait for a Spacebar keypress and keep the window open until then
    :param dict_for_df:
    :param Df:
    :param window:
    :return:
    """
    keyboard = io.devices.keyboard
    while True:
        dict_for_df['CurrentTime'] = round(time.time() - dict_for_df['StartTime'], 2)
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict_for_df])])
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == " ":
                return Df
            if event.key == "escape":
                graceful_quitting(window, params, Df, mini_df)
                window.close()
                core.quit()


def wait_for_joystick_press(window, Df: pandas.DataFrame, dict_for_df: dict, params=None, mini_df=None):
    pygame.init()
    joy = pygame.joystick.Joystick(0)
    joy.init()

    while True:
        dict_for_df['CurrentTime'] = round(time.time() - dict_for_df['StartTime'], 2)
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict_for_df])])
        core.wait(1 / 1000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                graceful_quitting(window, params, Df, mini_df)
                window.close()
                core.quit()
                break
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 7:
                    graceful_quitting(window, params, Df, mini_df)
                    window.close()
                    core.quit()
                else:
                    while True:
                        for currEvent in pygame.event.get():
                            if currEvent.type == pygame.JOYBUTTONUP:
                                return Df


def wait_for_space_with_replay(window, Df: pandas.DataFrame, dict_for_df: dict, io, params=None, mini_df=None):
    """
    Helper method to wait for a Spacebar keypress and keep the window open, or get 'r' keypress for replay of the
     InstructionsEnglish. Returns True if needed to replay.
    :param dict_for_df:
    :param Df:
    :param window:
    :return: True/False if r was pressed
    """
    keyboard = io.devices.keyboard
    while True:
        dict_for_df['CurrentTime'] = round(time.time() - dict_for_df['StartTime'], 2)
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict_for_df])])
        keys = keyboard.getPresses()
        for event in keys:
            if event.key == 'r' or event.key == 'R':
                return Df, True
            elif event.key == ' ':
                return Df, False
            elif event.key == "escape":
                graceful_quitting(window, params, Df, mini_df)
                window.close()
                core.quit()


def wait_for_joystick_press_with_replay(window, Df: pandas.DataFrame, dict_for_df: dict, params=None, mini_df=None):
    """
    Helper method to wait for a joystick keypress and keep the window open, or get 'r' keypress for replay of the
     InstructionsEnglish. Returns True if needed to replay.
    :param dict_for_df:
    :param Df:
    :param window:
    :return: True/False if r was pressed
    """
    pygame.init()
    joy = pygame.joystick.Joystick(0)
    joy.init()
    while True:
        dict_for_df['CurrentTime'] = round(time.time() - dict_for_df['StartTime'], 2)
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict_for_df])])
        core.wait(1 / 1000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                graceful_quitting(window, params, Df, mini_df)
                window.close()
                core.quit()
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 7:
                    graceful_quitting(window, params, Df, mini_df)
                    window.close()
                    core.quit()
                elif event.button == 1:
                    while True:
                        for currEvent in pygame.event.get():
                            if currEvent.type == pygame.JOYBUTTONUP:
                                return Df, True
                else:
                    while True:
                        for currEvent in pygame.event.get():
                            if currEvent.type == pygame.JOYBUTTONUP:
                                return Df, False


def wait_for_space_no_df(window, io, params=None, df=None, mini_df=None):
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
                graceful_quitting(window, params, df, mini_df)


def wait_for_joystick_no_df(window, params=None, df=None, mini_df=None):
    pygame.init()
    joy = pygame.joystick.Joystick(0)
    joy.init()
    while True:
        core.wait(1 / 1000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                graceful_quitting(window, params, df, mini_df)
                window.close()
                core.quit()
                break
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 7:
                    graceful_quitting(window, params, df, mini_df)
                    window.close()
                    core.quit()
                else:
                    while True:
                        for currEvent in pygame.event.get():
                            if currEvent.type == pygame.JOYBUTTONUP:
                                return


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
    if params["language"] == "Hebrew":
        scale = ratingscale.RatingScale(win,
                                        labels=[labels[0][::-1], labels[1][::-1]],  # Labels at the edges of the scale
                                        scale=None, choices=None, low=0, high=100, precision=1, tickHeight=0, size=2,
                                        textSize=0.6, acceptText='Continue', showValue=False, showAccept=True,
                                        markerColor="Yellow", acceptKeys=[" ", "space"], markerStart=50)
        textItem = visual.TextStim(win, text=text, height=.12, units='norm', pos=[0, 0.3], wrapWidth=2,
                                   languageStyle='RTL', font="Open Sans")

    else:
        scale = ratingscale.RatingScale(win,
                                        labels=[labels[0], labels[1]],  # Labels at the edges of the scale
                                        scale=None, choices=None, low=0, high=100, precision=1, tickHeight=0, size=2,
                                        textSize=0.6, acceptText='Continue', showValue=False, showAccept=True,
                                        markerColor="Yellow", acceptKeys=[" ", "space"], markerStart=50)
        textItem = visual.TextStim(win, text=text, height=.12, units='norm', pos=[0, 0.3], wrapWidth=2,
                                   languageStyle="LTR", font="Open Sans")

    dict_for_df = dataHandler.create_dict_for_df(params, Section='VAS', VASQuestionNumber=questionNo, Round=roundNo)
    while scale.noResponse:
        dict_for_df['CurrentTime'] = round(time.time() - dict_for_df['StartTime'], 2)
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict_for_df])])
        scale.draw()
        textItem.draw()
        win.flip()
        get_escape()
    return scale.getRating(), Df, dict_for_df


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
                           dict_for_df: dict):
    image = visual.ImageStim(win=window, image=imagePath, units='pix', size=(params['screenSize'][0],
                                                                             params['screenSize'][1]),
                             opacity=1)
    image.draw()
    window.update()
    key = event.getKeys()
    endTime = time.time() + timeframe
    while time.time() < endTime and 'space' not in key:
        dict_for_df['CurrentTime'] = round(time.time() - dict_for_df['StartTime'], 2)
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        key = event.getKeys()
    return Df


def display_image_until_key(window: visual.Window, params: dict, imagePath: str, key: str, Df: pandas.DataFrame,
                            dict_for_df: dict):
    image = visual.ImageStim(win=window, image=imagePath, units='pix', size=(params['screenSize'][0],
                                                                             params['screenSize'][1]),
                             opacity=1)
    image.draw()
    window.update()
    pressedKey = event.getKeys()
    while key not in pressedKey:
        dict_for_df['CurrentTime'] = round(time.time() - dict_for_df['StartTime'], 2)
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        pressedKey = event.getKeys()
    return Df


def graceful_quitting(window: visual.Window, params: dict, Df: pandas.DataFrame, miniDf=None):
    if Df is not None:
        dataHandler.export_raw_data(params, Df)
    if miniDf is not None:
        dataHandler.export_summarized_dataframe(params, miniDf)
    window.close()
    core.quit()


def countdown_before_door_open(window: visual.Window, image: visual.ImageStim, params: dict, df: pandas.DataFrame,
                               dict_for_df: dict):
    text_stim = visual.TextStim(window, text='3', pos=(0, 0), bold=True, height=75 * image.size[0])
    print(image.size)
    for i in [3, 2, 1]:
        text_stim.text = str(i)
        image.draw()
        text_stim.draw()
        window.flip()
        df = wait_for_time(1, df, dict_for_df)
    del text_stim
    image.draw()
    window.flip()
    return df


def wait_for_time(time_to_wait: float, df: pandas.DataFrame, dict_for_df: dict):
    start_time = time.time()
    while time.time() < start_time + time_to_wait:
        dict_for_df["CurrentTime"] = time.time()
        df = pandas.concat([df, pandas.DataFrame.from_records([dict_for_df])])
        core.wait(0.05)
    return df
