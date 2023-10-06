import random
import pandas
import sounddevice as sounddevice
from psychopy import core, visual, event
import time
import pygame
import helpers
from psychopy.iohub import launchHubServer
from psychopy.iohub.client.keyboard import Keyboard
from psychopy.visual import Window, MovieStim3, FINISHED
from psychopy import sound
import psychtoolbox as ptb

import serialHandler

MIN_LOCATION = -1.5
MAX_LOCATION = 1.75

MIDDLE_SUMMARY_STR1 = "בואו ננוח מעט. עד כה צברתם "
MIDDLE_SUMMARY_STR2Key = "מטבעות. לחצו על הרווח\n כשאתם מוכנים להמשיך."
MIDDLE_SUMMARY_STR2Joy = "מטבעות. לחצו על הג'ויסטיק\n כשאתם מוכנים להמשיך."

SOUNDS = {
    "lock": "./sounds/click_1s.wav",
    "reward": "./sounds/new_reward.mp3",
    "punishment": "./sounds/monster.wav"
}


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
    random.seed()
    if params['startingDistance'] == 'Random':
        location = round(random.uniform(MIN_LOCATION, MAX_LOCATION), 2)
    elif params['startingDistance'] == '40-60':
        location = round(random.uniform(MIN_LOCATION / 5, MAX_LOCATION / 5), 2)
    else:
        location = 0
    # isRandom = params['startingDistance'] == 'Random'
    # location = round(0.6 - 0.1 * random.random(), 2) if isRandom else 0  # a variable for the relative location
    # of the subject from the door, should be 0-1
    imagePath = params['doorImagePathPrefix'] + f"p{punishment}r{reward}" + params['imageSuffix']

    image = visual.ImageStim(window, image=imagePath,
                             size=((2 + location), (2 + location)),
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
    location = location + (units / 100)
    image.size = (2 + location, 2 + location)
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
                    # Dividing into segments by location, in order to get the motion smoother.
                    # If we're close to the door, the movements need to be a bit faster, and as we get back we need it
                    # Gradually get slower.
                    if 0.25 <= location < MAX_LOCATION:
                        image, location = move_screen(window, params, image, location,
                                                      params['sensitivity'] * 0.5 * 1.5)
                        Df = update_movement_in_df(dict, Df, location)
                    elif 0 <= location < 0.25:
                        image, location = move_screen(window, params, image, location,
                                                      params['sensitivity'] * 0.5 * 1.25)
                        Df = update_movement_in_df(dict, Df, location)
                    elif location < 0:
                        image, location = move_screen(window, params, image, location, params['sensitivity'] * 0.5)
                        Df = update_movement_in_df(dict, Df, location)
            elif event.key == 'down':
                downHold = True
                while downHold:
                    for releaseEvent in keyboard.getKeys(etype=Keyboard.KEY_RELEASE):
                        if releaseEvent == 'down':
                            downHold = False
                    # Dividing into segments corresponding with the "down" motion
                    if MIN_LOCATION < location < 0:
                        image, location = move_screen(window, params, image, location, params['sensitivity'] * (-0.5))
                        Df = update_movement_in_df(dict, Df, location)
                    elif 0 <= location <= 0.25:
                        image, location = move_screen(window, params, image, location,
                                                      params['sensitivity'] * (-0.5) * 1.25)
                        Df = update_movement_in_df(dict, Df, location)
                    elif location > 0.25:
                        image, location = move_screen(window, params, image, location,
                                                      params['sensitivity'] * (-0.5) * 1.5)
                        Df = update_movement_in_df(dict, Df, location)
            elif event.key == ' ' or event.key == 'space':
                space = True
                break

        Df = update_movement_in_df(dict, Df, location)
    location = normalize_location(location)
    return location, Df, dict, space  # NormalizedLocation


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

        if joystickMovement > 0.5 or joystickMovement < -0.5:
            speed = 2
        elif joystickMovement > 0.15 or joystickMovement < -0.15:
            speed = 1
        else:
            speed = 0

        if joystickMovement > 0 and MIN_LOCATION < location < 0:
            image, location = move_screen(window, params, image, location,
                                          params['sensitivity'] * -0.5 * speed)
        elif joystickMovement > 0 and 0 <= location < 0.25:
            image, location = move_screen(window, params, image, location,
                                          params['sensitivity'] * -0.5 * 1.25 * speed)
        elif joystickMovement > 0 and location >= 0.25:
            image, location = move_screen(window, params, image, location,
                                          params['sensitivity'] * -0.5 * 1.5 * speed)
        elif joystickMovement < 0 and 0.25 <= location < MAX_LOCATION:
            image, location = move_screen(window, params, image, location,
                                          params['sensitivity'] * 0.5 * 1.5 * speed)
        elif joystickMovement < 0 and 0 <= location < 0.25:
            image, location = move_screen(window, params, image, location,
                                          params['sensitivity'] * 0.5 * 1.25 * speed)
        elif joystickMovement < 0 and location < 0:
            image, location = move_screen(window, params, image, location,
                                          params['sensitivity'] * 0.5 * speed)

        Df = update_movement_in_df(dict, Df, location)
    location = normalize_location(location)
    return location, Df, dict, not joystickButton  # NormalizedLocation


def normalize_location(location: int):
    if location > MAX_LOCATION:
        location = MAX_LOCATION
    elif location < MIN_LOCATION:
        location = MIN_LOCATION
    if location > 0:
        locationNormalized = round((location * 100) / MAX_LOCATION)
    else:
        locationNormalized = round((location * 100) / (-1 * MIN_LOCATION))
    locationNormalized = round(locationNormalized / 2 + 50)
    return locationNormalized


def update_movement_in_df(dict: dict, Df: pandas.DataFrame, location):
    dict['CurrentTime'] = round(time.time() - dict['StartTime'], 3)
    locationNormalized = normalize_location(location)
    dict['CurrentDistance'] = locationNormalized
    if locationNormalized > dict['Distance_max']:
        dict['Distance_max'] = locationNormalized
    if locationNormalized < dict['Distance_min']:
        dict['Distance_min'] = locationNormalized

    # Update Df:
    Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
    return Df


def start_door(window: visual.Window, params, image: visual.ImageStim, reward: int, punishment: int, location,
               Df: pandas.DataFrame, dict: dict, io, scenarioIndex: int, miniDf: pandas.DataFrame, ser=None):
    # Set end time for 10s max
    start_time = time.time()
    end_time = start_time + 10
    if params['recordPhysio']:
        serialHandler.report_event(ser, scenarioIndex)
    # Add initial dict parameters
    dict['RoundStartTime'] = round(time.time() - dict['StartTime'], 3)
    dict['CurrentDistance'] = round((location + 1) * 50, 0)
    dict['Distance_max'] = round((location + 1) * 50, 0)
    dict['Distance_min'] = round((location + 1) * 50, 0)
    dict["ScenarioIndex"] = scenarioIndex
    Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
    dict.pop("ScenarioIndex")

    if params['keyboardMode']:
        location, Df, dict, lock = get_movement_input_keyboard(window, params, image, location, end_time, Df, dict, io,
                                                               miniDf)
    else:
        location, Df, dict, lock = get_movement_input_joystick(window, params, image, location, end_time, Df, dict,
                                                               miniDf)

    dict["ScenarioIndex"] = scenarioIndex + 50
    if params['recordPhysio']:
        serialHandler.report_event(ser, scenarioIndex + 50)
    total_time = time.time() - start_time
    dict["DistanceFromDoor_SubTrial"] = location
    dict['Distance_lock'] = 1 if lock else 0
    dict["DoorAction_RT"] = total_time * 1000
    dict["CurrentTime"] = round(time.time() - dict['StartTime'], 3)
    dict["ScenarioIndex"] = scenarioIndex + 50
    Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
    dict.pop("ScenarioIndex")

    # Seed randomization for waiting time and for door opening chance:
    random.seed(time.time() % 60)  # Seeding using the current second in order to have relatively random seed
    doorWaitTime = 2 + random.random() * 2  # Randomize waiting time between 2-4 seconds
    waitStart = time.time()
    dict["Door_anticipation_time"] = doorWaitTime * 1000

    if params['soundOn']:
        doorWaitTime -= 1
        play_sound("lock", 1, dict, Df)

    while time.time() < waitStart + doorWaitTime:
        dict["CurrentTime"] = round(time.time() - dict['StartTime'], 3)
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        core.wait(1 / 1000)

    # Randomize door opening chance according to location:
    doorOpenChance = random.random()
    isDoorOpening = doorOpenChance <= (location / 100)
    print(f"doorChance - {doorOpenChance}, location - {location / 100}, isOpening - {isDoorOpening}")

    if params['recordPhysio']:
        serialHandler.report_event(ser, scenarioIndex + 100)
    dict["Door_opened"] = 1 if isDoorOpening else 0
    dict["DoorStatus"] = 'opened' if isDoorOpening else 'closed'
    dict["CurrentTime"] = round(time.time() - dict['StartTime'], 3)
    dict["ScenarioIndex"] = scenarioIndex + 100
    Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
    dict.pop("ScenarioIndex")
    coins = 0

    if isDoorOpening:
        # Randomize the chances for p/r. If above 0.5 - reward. else - punishment.
        rewardChance = random.random()

        if rewardChance >= 0.5:
            outcomeString = f'{reward}_reward'
            coins = reward
            dict["DidWin"] = 1
            dict["Door_outcome"] = 'reward'
        else:
            outcomeString = f'{punishment}_punishment'
            coins = -1 * punishment
            dict["DidWin"] = 0
            dict["Door_outcome"] = 'punishment'

        outcomeImage = visual.ImageStim(window,
                                        image=params['outcomeImagePredix'] + outcomeString + params['imageSuffix'],
                                        size=(image.size[0] / 4, image.size[1] / 2.05),
                                        pos=(0, -0.059), units="norm", opacity=1)
        doorFrameImg = visual.ImageStim(window, image=params['doorImagePathPrefix'] + "doorOpens.png",
                                        size=(image.size[0] * 0.3, image.size[1] * 0.52),
                                        pos=(0.01, -0.1), units="norm", opacity=1)
        image.draw()
        outcomeImage.draw()
        doorFrameImg.draw()
        window.update()
        if params['soundOn']:
            play_sound(dict["Door_outcome"], 2.5, dict, Df)
        else:
            waitTimeStart = time.time()
            while time.time() < waitTimeStart + 2:
                dict["CurrentTime"] = round(time.time() - dict['StartTime'], 3)
                Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
                core.wait(1 / 1000)

        del outcomeImage
        del doorFrameImg
        window.update()

    image.setImage('./img/iti.jpg')
    image.setSize((3.2, 3.2))
    image.draw()
    window.update()
    start_time = time.time()
    iti_time = 2 + random.random() * 2
    while time.time() < start_time + iti_time:
        dict["CurrentTime"] = round(time.time() - dict['StartTime'], 3)
        dict["ITI_duration"] = iti_time
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        image.size += 0.05
        image.draw()
        window.update()
        core.wait(0.03)

    return coins, total_time, Df, dict, lock


def show_screen_pre_match(window: visual.Window, params: dict, session: int, io, coins=0):
    if session == 2 or session == 3:
        if params["keyboardMode"]:
            message = visual.TextStim(window,
                                      text=MIDDLE_SUMMARY_STR1 + f"{coins}" + "\n" + MIDDLE_SUMMARY_STR2Key,
                                      units="norm",
                                      color=(255, 255, 255), languageStyle='RTL')
        else:
            message = visual.TextStim(window,
                                      text=MIDDLE_SUMMARY_STR1 + f"{coins}" + "\n" + MIDDLE_SUMMARY_STR2Joy,
                                      units="norm",
                                      color=(255, 255, 255), languageStyle='RTL')
        message.draw()

    else:
        screenNames = ["practice_start", "start_main_game"]
        image = visual.ImageStim(win=window, units="norm", opacity=1, size=(2, 2))
        image.image = "./img/InstructionsHebrew/" + screenNames[session] + ".jpeg"
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
    image.image = "./img/instructionsHebrew/BeforeWheel.jpg"
    image.draw()
    window.update()

    if params["keyboardMode"]:
        helpers.wait_for_space_no_df(window, io)
    else:
        helpers.wait_for_joystick_no_df(window)

    movie = visual.MovieStim3(window, filename=r'./img/Spin16.mp4', size=(2, 2), units="norm")

    while movie.status != FINISHED:
        movie.draw()
        window.flip()

    if params["keyboardMode"]:
        helpers.wait_for_space_no_df(window, io)
    else:
        helpers.wait_for_joystick_no_df(window)

    return


def play_sound(soundType: str, waitTime: float, dict: dict, Df: pandas.DataFrame):
    """
    The method plays a sound and sleeps through it, while recording data for the DF
    """

    soundToPlay = sound.Sound(SOUNDS[soundType])
    now = ptb.GetSecs()
    soundToPlay.play(when=now)
    startTime = time.time()
    while time.time() < startTime + waitTime:
        dict["CurrentTime"] = round(time.time() - dict['StartTime'], 3)
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        core.wait(1 / 1000)
    soundToPlay.stop()
