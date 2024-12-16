import time
import pygame
from psychopy import core, event, visual
from psychopy.iohub import launchHubServer
from psychopy.iohub.client.keyboard import Keyboard
from psychopy.visual import ratingscale
import dataHandler
import pandas
import datetime


def wait_for_space(window, io, params=None, mini_df=None, summary_df=None):
    """
    Helper method to wait for a Spacebar keypress and keep the window open until then
    :param dict_for_df:
    :param Df:
    :param window:
    :return:
    """
    keyboard = io.devices.keyboard
    while True:
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == " ":
                return
            if event.key == "escape":
                graceful_quitting(window, params, mini_df, summary_df)
                window.close()
                core.quit()


def wait_for_joystick_press(window, params=None, mini_df=None, summary_df=None):
    pygame.init()
    joy = pygame.joystick.Joystick(0)
    joy.init()

    while True:
        core.wait(1 / 1000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                graceful_quitting(window, params, mini_df, summary_df)
                window.close()
                core.quit()
                break
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 7:
                    graceful_quitting(window, params, mini_df, summary_df)
                    window.close()
                    core.quit()
                else:
                    while True:
                        for currEvent in pygame.event.get():
                            if currEvent.type == pygame.JOYBUTTONUP:
                                return


def wait_for_space_with_replay(window, io, params=None, mini_df=None, summary_df=None):
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
        keys = keyboard.getPresses()
        for event in keys:
            if event.key == 'r' or event.key == 'R':
                return True
            elif event.key == ' ':
                return False
            elif event.key == "escape":
                graceful_quitting(window, params, mini_df, summary_df)
                window.close()
                core.quit()


def wait_for_joystick_press_with_replay(window, params=None, mini_df=None, summary_df=None):
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
        core.wait(1 / 1000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                graceful_quitting(window, params, mini_df, summary_df)
                window.close()
                core.quit()
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 7:
                    graceful_quitting(window, params, mini_df, summary_df)
                    window.close()
                    core.quit()
                elif event.button == 1:
                    while True:
                        for currEvent in pygame.event.get():
                            if currEvent.type == pygame.JOYBUTTONUP:
                                return True
                else:
                    while True:
                        for currEvent in pygame.event.get():
                            if currEvent.type == pygame.JOYBUTTONUP:
                                return False


def wait_for_space_no_df(window, io, params=None, mini_df=None, summary_df=None):
    """
    Helper method to wait for a Spacebar keypress and keep the window open, without writing to Df.
    :param window:
    :return:
    """
    keyboard = io.devices.keyboard
    keyboard.getKeys()
    core.wait(0.1)
    while True:
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == " ":
                return
            if event.key == "escape":
                graceful_quitting(window, params, mini_df, summary_df)


def wait_for_joystick_no_df(window, params=None, mini_df=None, summary_df=None):
    pygame.init()
    joy = pygame.joystick.Joystick(0)
    joy.init()
    core.wait(0.1)
    while True:
        core.wait(1 / 1000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                graceful_quitting(window, params, mini_df, summary_df)
                window.close()
                core.quit()
                break
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 7:
                    graceful_quitting(window, params, mini_df, summary_df)
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


def display_vas(win, params, text, labels, questionNo: int, roundNo: int, io):
    """
    A helper method that displays VAS question (text object) and places a scale using psychopy.visual.ratingscale.
    The scale goes between two labels, and the answer (1-100) is saved to Df, along with the response time
    :param roundNo:
    :param questionNo:
    :param win:
    :param params:
    :param text:
    :param labels:
    :return: The VAS rating, along with the Dataframe and dict
    """

    keyboard = io.devices.keyboard
    keyboard.getKeys()

    if params["language"] == "Hebrew":
        scale = ratingscale.RatingScale(win,
                                        labels=[labels[0][::-1], labels[1][::-1]],  # Labels at the edges of the scale
                                        scale=None, choices=None, low=0, high=10, precision=1, tickHeight=0, size=2,
                                        textSize=0.6, acceptText='Continue', showValue=False, showAccept=True,
                                        markerColor="Yellow", acceptKeys=[" ", "space"], markerStart=5,
                                        noMouse=True, leftKeys='left', rightKeys='right', acceptPreText="לחצו על הרווח"[::-1],
                                        acceptSize=1.5)
        textItem = visual.TextStim(win, text=text, height=.12, units='norm', pos=[0, 0.3], wrapWidth=2,
                                   languageStyle='RTL', font="Open Sans")

    else:
        scale = ratingscale.RatingScale(win,
                                        labels=[labels[0], labels[1]],  # Labels at the edges of the scale
                                        scale=None, choices=None, low=0, high=10, precision=1, tickHeight=0, size=2,
                                        textSize=0.6, acceptText='Continue', showValue=False, showAccept=True,
                                        markerColor="Yellow", acceptKeys=[" ", "space"], markerStart=5,
                                        noMouse=True, leftKeys='left', rightKeys='right', acceptPreText="Press Spacebar",
                                        acceptSize=1.5)
        textItem = visual.TextStim(win, text=text, height=.12, units='norm', pos=[0, 0.3], wrapWidth=2,
                                   languageStyle="LTR", font="Open Sans")

    dict_for_df = dataHandler.create_dict_for_df(params, Section='VAS', VASQuestionNumber=questionNo, Round=roundNo)

    core.wait(0.05)
    keyboard.getKeys()

    while scale.noResponse:

        scale.draw()
        textItem.draw()
        win.mouseVisible = False
        win.flip()
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            #TODO: Add graceful quitting
            if event.key == "escape":
                win.close()
                core.quit()

            core.wait(0.05)

    return scale.getRating(), dict_for_df


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
    window.mouseVisible = False
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
    window.mouseVisible = False
    window.update()
    pressedKey = event.getKeys()
    while key not in pressedKey:
        dict_for_df['CurrentTime'] = round(time.time() - dict_for_df['StartTime'], 2)
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        pressedKey = event.getKeys()
    return Df


def graceful_quitting(window: visual.Window, params: dict, miniDf=None, summary_df=None):
    dataHandler.export_data(params, miniDF=miniDf, summary=summary_df)
    window.close()
    core.quit()


def countdown_before_door_open(window: visual.Window, image: visual.ImageStim, params: dict, df: pandas.DataFrame,
                               dict_for_df: dict):
    text_stim = visual.TextStim(window, text='3', pos=(0, 0), bold=True, height=40 * image.size[0], color='black')
    print(image.size)
    for i in [3, 2, 1]:
        text_stim.text = str(i)
        image.draw()
        text_stim.draw()
        window.mouseVisible = False
        window.flip()
        df = wait_for_time(1, df, dict_for_df)
    del text_stim
    image.draw()
    window.mouseVisible = False
    window.flip()
    df = wait_for_time(1, df, dict_for_df)
    return df


def wait_for_time(time_to_wait: float):
    start_time = time.time()
    while time.time() < start_time + time_to_wait:
        core.wait(0.05)
    return

def show_version_specific_message(window: visual.Window, params: dict, block:int, io):
    cond = "act" if params["ACTBlock"] == block else "neut"
    if params["screamVersion"]:
        if cond == "neut" and block == 1:
            path = f"./img/versionSpecificInstructions/scream_neut_1_{params['language'][0]}.jpeg"
        elif cond == "neut" and block == 2:
            path = f"./img/versionSpecificInstructions/scream_neut_2_{params['language'][0]}.jpeg"
        else:
            path = f"./img/versionSpecificInstructions/scream_{cond}_{params['language'][0]}.jpeg"
    elif params["cameraVersion"]:
        path = f"./img/versionSpecificInstructions/camera_{cond}_{params['language'][0]}.jpeg"
    elif params["highValue"]:
        path = f"./img/versionSpecificInstructions/high_value_{cond}_{params['language'][0]}.jpeg"
    else:
        return
    image = visual.ImageStim(window, image=path, size=(2,2), units='norm')
    image.draw()
    window.mouseVisible = False
    window.update()
    if params['keyboardMode']:
        wait_for_space_no_df(window, io)
    else:
        wait_for_joystick_no_df(window)
