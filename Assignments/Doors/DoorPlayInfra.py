import random
import pandas
from psychopy import core, visual, event
import time
import pygame
import helpers
from psychopy.iohub import launchHubServer
from psychopy.iohub.client.keyboard import Keyboard
from psychopy.visual import Window, MovieStim3, FINISHED


def setup_door(window, params, reward: int, punishment: int):
    """
    Show door corresponding to the reward and punishment sent as arguments. Chooses the size in which it starts
    either randomly or fixed according to the parameters in order to be able to zoom out nicely.
    :param params: parameters from the main run
    :param window: psychopy windows object
    :param reward: reward (1-7)
    :param punishment: punishment (1-7)
    :return: image: the image object that will be used for movements
    :return: location: the relative location of the subject from the door, should be 1-100
    """
    isRandom = params['startingDistance'] == 'Random'
    location = round(0.6 - 0.1 * random.random(), 2) if isRandom else params[
                                                                          'startingDistance'] / 100  # a variable for the relative location
    # of the subject from the door, should be 0-1
    imagePath = params['doorImagePathPrefix'] + f"p{punishment}r{reward}" + params['imageSuffix']

    image = visual.ImageStim(window, image=imagePath,
                             size=((1.5 + location), (1.5 + location)),
                             units="norm", opacity=1)
    image.draw()

    window.update()
    return image, location


def move_screen(window, params, image: visual.ImageStim, location, units):
    """
    The method brings the image closer or further from the subject, according to the units of movement given.
    The units are converted from 1-100 to 0-1, and added to the location.
    :param window:
    :param params:
    :param image:
    :param location:
    :param units:
    :return: image: the updated image object
    :return: location: the updated location. Will be used to determine the chance of the door opening.
    """
    location = location + units / 100
    image.size = (1.5 + location, 1.5 + location)
    image.draw()
    window.update()
    return image, location


def get_movement_input_keyboard(window, params, image: visual.ImageStim, location, end_time: time.time,
                                Df: pandas.DataFrame, dict: dict, io, miniDf: pandas.DataFrame):
    """
    The method gets up/down key state and moves the screen accordingly.
    The method requires pygame to be installed (and therefore imported to Psychopy if needed).
    :param dict:
    :param Df:
    :param window:
    :param params:
    :param image:
    :param location:
    :param end_time:
    :return: location, Df and dictionary
    """

    keyboard = io.devices.keyboard
    keyboard.clearEvents()
    space = False
    while time.time() < end_time and not space:
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == "escape":
                helpers.graceful_quitting(window, params, Df, miniDf)
                window.close()
                core.quit()
            if event.key == 'up':
                upHold = True
                while upHold:
                    for releaseEvent in keyboard.getKeys(etype=Keyboard.KEY_RELEASE):
                        if releaseEvent.key == 'up':
                            upHold = False
                    if location < 0.99:
                        image, location = move_screen(window, params, image, location, params['sensitivity'] * 0.5)
                        Df = update_movement_in_df(dict, Df, location)
            elif event.key == 'down':
                downHold = True
                while downHold:
                    for releaseEvent in keyboard.getKeys(etype=Keyboard.KEY_RELEASE):
                        if releaseEvent == 'down':
                            downHold = False
                    if location > 0.01:
                        image, location = move_screen(window, params, image, location, params['sensitivity'] * (-0.5))
                        Df = update_movement_in_df(dict, Df, location)
            elif event.key == ' ' or event.key == 'space':
                space = True
                break

        Df = update_movement_in_df(dict, Df, location)

    return location, Df, dict, space


def get_movement_input_joystick(window, params, image: visual.ImageStim, location, end_time: time.time,
                                Df: pandas.DataFrame, dict: dict, miniDf: pandas.DataFrame):
    pygame.init()
    joy = pygame.joystick.Joystick(0)
    joy.init()
    joystickButton = False
    while time.time() < end_time and not joystickButton:

        for event in pygame.event.get():
            if joystickButton:
                break
            if event.type == pygame.QUIT:
                helpers.graceful_quitting(window, params, Df, miniDf)
                window.close()
                core.quit()
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 7:
                    helpers.graceful_quitting(window, params, Df, miniDf)
                    window.close()
                    core.quit()
                elif event.button == 0:
                    joystickButton = True

        joystickMovement = joy.get_axis(1)
        if (joystickMovement > 0.15 and 0.01 < location) or (joystickMovement < -0.15 and location < 0.99):
            image, location = move_screen(window, params, image, location,
                                          params['sensitivity'] * joystickMovement * -1)

        Df = update_movement_in_df(dict, Df, location)

    return location, Df, dict, not joystickButton


def update_movement_in_df(dict: dict, Df: pandas.DataFrame, location):
    dict['CurrentTime'] = round(time.time() - dict['StartTime'], 3)
    dict['CurrentDistance'] = round(location, 2) * 100
    if location > dict['Distance_max']:
        dict['Distance_max'] = round(location, 2) * 100
    if location < dict['Distance_min']:
        dict['Distance_min'] = round(location, 2) * 100

    # Update Df:
    Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
    return Df


def start_door(window: visual.Window, params, image: visual.ImageStim, reward: int, punishment: int, location,
               Df: pandas.DataFrame, dict: dict, io, scenarioIndex: int, miniDf: pandas.DataFrame, ser=None):
    # Set end time for 10s max
    start_time = time.time()
    end_time = start_time + 10
    if params['recordPhysio']:
        ser.write(bin(scenarioIndex))
    # Add initial dict parameters
    dict['RoundStartTime'] = round(time.time() - dict['StartTime'], 3)
    dict['CurrentDistance'] = round(location, 2) * 100
    dict['Distance_max'] = round(location, 2) * 100
    dict['Distance_min'] = round(location, 2) * 100
    dict["ScenarioIndex"] = scenarioIndex
    Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
    dict.pop("ScenarioIndex")

    if params['keyboardMode']:
        location, Df, dict, lock = get_movement_input_keyboard(window, params, image, location, end_time, Df, dict, io,
                                                               miniDf)
    else:
        location, Df, dict, lock = get_movement_input_joystick(window, params, image, location, end_time, Df, dict,
                                                               miniDf)

    if params['recordPhysio']:
        ser.write(bin(scenarioIndex + 50))
    total_time = time.time() - start_time
    dict["DistanceAtLock"] = round(location, 2) * 100
    dict['Distance_lock'] = 1 if lock else 0
    dict["LockTime"] = total_time * 1000
    dict["CurrentTime"] = round(time.time() - dict['StartTime'], 3)
    dict["ScenarioIndex"] = scenarioIndex + 50
    Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
    dict.pop("ScenarioIndex")

    # Seed randomization for waiting time and for door opening chance:
    random.seed(time.time() % 60)  # Seeding using the current second in order to have relatively random seed
    doorWaitTime = 2 + random.random() * 2  # Randomize waiting time between 2-4 seconds
    waitStart = time.time()

    dict["DoorWaitTime"] = doorWaitTime * 1000
    while time.time() < waitStart + doorWaitTime:
        dict["CurrentTime"] = round(time.time() - dict['StartTime'], 3)
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        core.wait(1 / 1000)

    # Randomize door opening chance according to location:
    doorOpenChance = random.random()
    isDoorOpening = doorOpenChance <= location

    if params['recordPhysio']:
        ser.write(bin(scenarioIndex + 100))
    dict["DidDoorOpen"] = 1 if isDoorOpening else 0
    dict["DoorStatus"] = 'opened' if isDoorOpening else 'closed'
    dict["CurrentTime"] = round(time.time() - dict['StartTime'], 3)
    dict["ScenarioIndex"] = scenarioIndex + 100
    Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
    dict.pop("ScenarioIndex")

    if isDoorOpening:
        # Randomize the chances for p/r. If above 0.5 - reward. else - punishment.
        rewardChance = random.random()

        if rewardChance >= 0.5:
            outcomeString = f'{reward}_reward'
            coins = reward
            dict["DidWin"] = 1
            dict["DoorOutcome"] = 'reward'
        else:
            outcomeString = f'{punishment}_punishment'
            coins = -1 * punishment
            dict["DidWin"] = 0
            dict["DoorOutcome"] = 'punishment'

        outcomeImage = visual.ImageStim(window, image=params['outcomeImagePredix'] + outcomeString + params['imageSuffix'],
                                size=(image.size[0] / 4, image.size[1] / 2.1),
                                pos=(0, -0.057), units="norm", opacity=1)
        doorFrameImg = visual.ImageStim(window, image=params['doorImagePathPrefix'] + "doorOpens.png",
                                        size=(image.size[0] * 0.3, image.size[1] * 0.52),
                                        pos=(0.009, -0.1), units="norm", opacity=1)
        image.draw()
        outcomeImage.draw()
        doorFrameImg.draw()
        window.update()
        waitTimeStart = time.time()
        while time.time() < waitTimeStart + 2:
            dict["CurrentTime"] = round(time.time() - dict['StartTime'], 3)
            Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
            core.wait(1 / 1000)

        del outcomeImage
        del doorFrameImg
        window.update()

        return coins, total_time, Df, dict, lock

    else:
        return 0, total_time, Df, dict, lock


def show_screen_pre_match(window: visual.Window, params: dict, session: int, io, coins=0):
    if session == 2:
        if params["keyboardMode"]:
            message = visual.TextStim(window,
                                      text=f"Let’s rest for a bit. You have {coins} coins. Press Space when you "
                                           f"are ready to keep playing.", units="norm", color=(255, 255, 255))
        else:
            message = visual.TextStim(window, text=f"Let’s rest for a bit. You have {coins} coins. Click when you "
                                                   f"are ready to keep playing.", units="norm", color=(255, 255, 255))
        message.draw()

    else:
        screenNames = ["practice_start", "start_main_game"]
        image = visual.ImageStim(win=window, units="norm", opacity=1, size=(2, 2))
        image.image = "./img/instructions/" + screenNames[session] + ".jpg"
        image.draw()

    window.update()
    if params["keyboardMode"]:
        helpers.wait_for_space_no_df(window, io)
    else:
        helpers.wait_for_joystick_no_df(window)

    if session == 1:
        show_wheel(window, params, io)


def show_wheel(window: visual.Window, params: dict, io=None):
    image = visual.ImageStim(win=window, units="norm", opacity=1, size=(2, 2))
    image.image = "./img/instructions/BeforeWheel.jpg"
    image.draw()
    window.update()

    if params["keyboardMode"]:
        helpers.wait_for_space_no_df(window, io)
    else:
        helpers.wait_for_joystick_no_df(window)

    movie = visual.MovieStim3(window, filename=r'./img/16_Coins.mp4', size=(2, 2), units="norm")

    while movie.status != FINISHED:
        movie.draw()
        window.flip()

    if params["keyboardMode"]:
        helpers.wait_for_space_no_df(window, io)
    else:
        helpers.wait_for_joystick_no_df(window)

    return
