import random
import pandas
import pandas as pd
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
import sys
import inspect

import serialHandler

MIN_LOCATION = -1.5
MAX_LOCATION = 1.75

WAIT_TIME_ON_DOOR = 4

MIDDLE_SUMMARY_STR1_HE = "בואו ננוח מעט.\n"
MIDDLE_SUMMARY_STR2Key_HE = "לחצו על הרווח כשאתם מוכנים להמשיך."
MIDDLE_SUMMARY_STR2Joy_HE = "לחצו על הג'ויסטיק כשאתם מוכנים להמשיך."

MIDDLE_SUMMARY_STR1_EN = "Let's rest a bit.\n"
MIDDLE_SUMMARY_STR2Key_EN = "Press the spacebar when you're ready."
MIDDLE_SUMMARY_STR2Joy_EN = "Press the joystick when you're ready."

FINAL_SUMMARY_STR1_EN = "You scored "
FINAL_SUMMARY_STR2_EN = "Coins!\n Well done!\n\nThank you for your participation."

FINAL_SUMMARY_STR1_HE = "צברת "
FINAL_SUMMARY_STR2_HE = "מטבעות\n כל הכבוד!\n\n תודה על השתתפותך בניסוי."

SOUNDS = {
    "lock": "./sounds/click_1s.wav",
    "reward": "./sounds/new_reward.mp3",
    "punishment": "./sounds/monster.mp3",
    "beep": "./sounds/beep_for_anticipation.mp3"
}


def setup_door(window, images, params, reward: int, punishment: int):
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

    print(f"Reward - {reward}, Punishment - {punishment}")
    if reward == 0 and punishment == 0:
        image = images[0]
    else:
        image = images[(reward - 1) * 7 + punishment]
    image.setSize((2 + location, 2 + location))
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
                                full_df: pandas.DataFrame, dict_for_df: dict, io, mini_df: pandas.DataFrame, summary_df=None):
    """
    The method gets up/down key state and moves the screen accordingly.
    The method requires pygame to be installed (and therefore imported to Psychopy if needed).
    :param dict_for_df:
    :param full_df:
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
                helpers.graceful_quitting(window, params, full_df, mini_df, summary_df)
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
                        if params['saveFullDF']:
                            full_df = update_movement_in_df(dict_for_df, full_df, location)
                    elif 0 <= location < 0.25:
                        image, location = move_screen(window, params, image, location,
                                                      params['sensitivity'] * 0.5 * 1.25)
                        if params['saveFullDF']:
                            full_df = update_movement_in_df(dict_for_df, full_df, location)
                    elif location < 0:
                        image, location = move_screen(window, params, image, location, params['sensitivity'] * 0.5)
                        if params['saveFullDF']:
                            full_df = update_movement_in_df(dict_for_df, full_df, location)
            elif event.key == 'down':
                downHold = True
                while downHold:
                    for releaseEvent in keyboard.getKeys(etype=Keyboard.KEY_RELEASE):
                        if releaseEvent == 'down':
                            downHold = False
                    # Dividing into segments corresponding with the "down" motion
                    if MIN_LOCATION < location < 0:
                        image, location = move_screen(window, params, image, location, params['sensitivity'] * (-0.5))
                        if params['saveFullDF']:
                            full_df = update_movement_in_df(dict_for_df, full_df, location)
                    elif 0 <= location <= 0.25:
                        image, location = move_screen(window, params, image, location,
                                                      params['sensitivity'] * (-0.5) * 1.25)
                        if params['saveFullDF']:
                            full_df = update_movement_in_df(dict_for_df, full_df, location)
                    elif location > 0.25:
                        image, location = move_screen(window, params, image, location,
                                                      params['sensitivity'] * (-0.5) * 1.5)
                        if params['saveFullDF']:
                            full_df = update_movement_in_df(dict_for_df, full_df, location)
            elif event.key == ' ' or event.key == 'space':
                space = True
                break
        core.wait(0.05)
        if params['saveFullDF']:
            full_df = update_movement_in_df(dict_for_df, full_df, location)
    location = normalize_location(location)
    return location, full_df, dict_for_df, space  # NormalizedLocation


def get_movement_input_joystick(window, params, image: visual.ImageStim, location, end_time: time.time,
                                full_df: pandas.DataFrame, dict_for_df: dict, mini_df: pandas.DataFrame, summary_df=None):
    pygame.init()
    joy = pygame.joystick.Joystick(0)
    joy.init()
    joystickButton = False
    while time.time() < end_time and not joystickButton:

        for event in pygame.event.get():
            if joystickButton:
                break
            if event.type == pygame.QUIT:
                helpers.graceful_quitting(window, params, full_df, mini_df, summary_df)
                window.close()
                core.quit()
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 7:
                    helpers.graceful_quitting(window, params, full_df, mini_df, summary_df)
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

        if params['saveFullDF']:
            full_df = update_movement_in_df(dict_for_df, full_df, location)
        core.wait(0.05)
    location = normalize_location(location)
    return location, full_df, dict_for_df, not joystickButton  # NormalizedLocation


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


def update_movement_in_df(dict_for_df: dict, Df: pandas.DataFrame, location):
    dict_for_df['CurrentTime'] = round(time.time() - dict_for_df['StartTime'], 2)
    locationNormalized = normalize_location(location)
    dict_for_df['CurrentDistance'] = locationNormalized
    if locationNormalized > dict_for_df['Distance_max']:
        dict_for_df['Distance_max'] = locationNormalized
    if locationNormalized < dict_for_df['Distance_min']:
        dict_for_df['Distance_min'] = locationNormalized

    # Update Df:
    Df = pandas.concat([Df, pandas.DataFrame.from_records([dict_for_df])])
    return Df


def start_door(window: visual.Window, params, image: visual.ImageStim, reward: int, punishment: int, total_coins: int,
               location,
               full_df: pandas.DataFrame, dict_for_df: dict, io, scenarioIndex: int, mini_df: pandas.DataFrame,
               summary_df=None, ser=None, simulation=False):
    # Set end time for 10s max
    start_time = time.time()
    end_time = start_time + 10

    # Add initial dict parameters
    dict_for_df['RoundStartTime'] = round(time.time() - dict_for_df['StartTime'], 2)
    dict_for_df['CurrentDistance'] = round((location + 1) * 50, 0)
    dict_for_df['Distance_max'] = round((location + 1) * 50, 0)
    dict_for_df['Distance_min'] = round((location + 1) * 50, 0)
    if not simulation and reward != 0:
        dict_for_df["ScenarioIndex"] = scenarioIndex
    dict_for_df["Total_coins"] = total_coins
    if params['saveFullDF']:
        full_df = pandas.concat([full_df, pandas.DataFrame.from_records([dict_for_df])])
    if not params['reducedEvents']:
        mini_df = pandas.concat([mini_df, pandas.DataFrame.from_records([dict_for_df])])
        dict_for_df.pop("ScenarioIndex")

    if params['keyboardMode']:
        location, full_df, dict_for_df, lock = get_movement_input_keyboard(window, params, image, location, end_time, full_df,
                                                                           dict_for_df, io,
                                                                           mini_df, summary_df)
    else:
        location, full_df, dict_for_df, lock = get_movement_input_joystick(window, params, image, location, end_time, full_df,
                                                                           dict_for_df,
                                                                           mini_df, summary_df)

    if not params['reducedEvents'] and not simulation:
        dict_for_df["ScenarioIndex"] = scenarioIndex + 50
        if params['recordPhysio'] and not simulation:
            serialHandler.report_event(ser, dict_for_df["ScenarioIndex"])
    total_time = time.time() - start_time
    dict_for_df["DistanceFromDoor_SubTrial"] = location
    dict_for_df['Distance_lock'] = 1 if lock else 0
    dict_for_df["DoorAction_RT"] = round(total_time * 1000, 2) if total_time < 10 else 10
    dict_for_df["CurrentTime"] = round(time.time() - dict_for_df['StartTime'], 2)
    if params['saveFullDF']:
        full_df = pandas.concat([full_df, pandas.DataFrame.from_records([dict_for_df])])
    if not params['reducedEvents'] and not simulation:
        mini_df = pandas.concat([mini_df, pandas.DataFrame.from_records([dict_for_df])])
        dict_for_df.pop("ScenarioIndex")

    # Seed randomization for waiting time and for door opening chance:
    random.seed(time.time() % 60)  # Seeding using the current second in order to have relatively random seed
    doorWaitTime = 3 + random.random()  # Randomize waiting time between 3-4 seconds
    dict_for_df["Door_anticipation_time"] = doorWaitTime * 1000

    if params['soundOn']:
        play_sound(params, "lock", 0.5, dict_for_df, full_df, volume=0.7)
        if params['beeps']:
            doorWaitTime -= 2
        else:
            doorWaitTime -= 3

    waitStart = time.time()
    while time.time() < waitStart + doorWaitTime:
        if params['saveFullDF']:
            dict_for_df["CurrentTime"] = round(time.time() - dict_for_df['StartTime'], 2)
            full_df = pandas.concat([full_df, pandas.DataFrame.from_records([dict_for_df])])
        core.wait(1 / 100)

    if params["soundOn"] and params['beeps']:
        full_df = play_sound(params, "beep", 2, dict_for_df, full_df)
    else:
        helpers.wait_for_time(3, full_df, dict_for_df)
        # Df = helpers.countdown_before_door_open(window, image, params, Df, dict_for_df,)

    # Randomize door opening chance according to location:
    doorOpenChance = random.random()
    isDoorOpening = doorOpenChance <= (location / 100)
    print(f"doorChance - {doorOpenChance}, location - {location / 100}, isOpening - {isDoorOpening}")

    if not params['reducedEvents'] and not simulation:
        dict_for_df["ScenarioIndex"] = scenarioIndex + 100
        if params['recordPhysio'] and not simulation:
            serialHandler.report_event(ser, scenarioIndex + 100)
    dict_for_df["Door_opened"] = 1 if isDoorOpening else 0
    dict_for_df["DoorStatus"] = 'opened' if isDoorOpening else 'closed'
    dict_for_df["CurrentTime"] = round(time.time() - dict_for_df['StartTime'], 2)
    dict_for_df["Total_coins"] = total_coins
    if params['saveFullDF']:
        full_df = pandas.concat([full_df, pandas.DataFrame.from_records([dict_for_df])])
    coins = 0

    if isDoorOpening:
        # Randomize the chances for p/r. If above 0.5 - reward. else - punishment.
        rewardChance = random.random()

        if rewardChance >= 0.5:
            # outcomeString = f'{reward}_reward'
            outcome_string = "reward" if not params['outcomeString'] else f"reward_{reward}"
            coins = reward
            dict_for_df["DidWin"] = 1
            dict_for_df["Door_outcome"] = 'reward'
        else:
            # outcomeString = f'{punishment}_punishment'
            outcome_string = "punishment" if not params['outcomeString'] else f"punishment_{punishment}"
            coins = -1 * punishment
            dict_for_df["DidWin"] = 0
            dict_for_df["Door_outcome"] = 'punishment'

        doorFrameImg = visual.ImageStim(window, image=params['doorOutcomePath'] + outcome_string + ".png",
                                        size=(image.size[0], image.size[1]),
                                        pos=(0, 0), units="norm", opacity=1)
        image.draw()
        # outcomeImage.draw()
        doorFrameImg.draw()
        window.update()

        dict_for_df["Total_coins"] += coins
        mini_df = pandas.concat([mini_df, pandas.DataFrame.from_records([dict_for_df])])

        if params['soundOn']:
            full_df = play_sound(params, dict_for_df["Door_outcome"], WAIT_TIME_ON_DOOR, dict_for_df, full_df)
        else:
            waitTimeStart = time.time()
            while time.time() < waitTimeStart + WAIT_TIME_ON_DOOR:
                if params['saveFullDF']:
                    dict_for_df["CurrentTime"] = round(time.time() - dict_for_df['StartTime'], 2)
                    full_df = pandas.concat([full_df, pandas.DataFrame.from_records([dict_for_df])])
                core.wait(1 / 1000)

        # del outcomeImage
        del doorFrameImg
        window.update()

    else:
        mini_df = pandas.concat([mini_df, pandas.DataFrame.from_records([dict_for_df])])

        doorFrameImg = visual.ImageStim(window, image=params['doorImagePathPrefix'] + 'lock' + ".png",
                                        size=(image.size[0], image.size[1]),
                                        pos=(0, 0), units="norm", opacity=1)
        image.draw()
        doorFrameImg.draw()
        window.update()

        waitTimeStart = time.time()
        while time.time() < waitTimeStart + WAIT_TIME_ON_DOOR:
            if params['saveFullDF']:
                dict_for_df["CurrentTime"] = round(time.time() - dict_for_df['StartTime'], 2)
                full_df = pandas.concat([full_df, pandas.DataFrame.from_records([dict_for_df])])
            core.wait(1 / 1000)

        del doorFrameImg
        window.update()

    iti_image = visual.ImageStim(win=window, image='./img/iti.jpg', units="norm", opacity=1)
    iti_image.setSize((3.2, 3.2))
    iti_image.draw()
    window.update()
    start_time = time.time()

    iti_time = random.uniform(params['ITIDurationMin'], params['ITIDurationMax'])
    print(f"ITI Set time - {iti_time}")

    while time.time() < start_time + iti_time:
        dict_for_df["CurrentTime"] = round(time.time() - dict_for_df['StartTime'], 2)
        dict_for_df["ITI_duration"] = iti_time
        if params['saveFullDF']:
            full_df = pandas.concat([full_df, pandas.DataFrame.from_records([dict_for_df])])
        iti_image.size += 0.05
        iti_image.draw()
        window.update()
        core.wait(0.03)
    print(f'ITI Actual time - {time.time() - start_time}')
    del iti_image
    image.setSize((2,2))

    return coins, total_time, full_df, mini_df, dict_for_df, lock


def show_screen_pre_match(window: visual.Window, params: dict, session: int, io, df: pd.DataFrame,
                          mini_df: pd.DataFrame,
                          summary_df: pd.DataFrame, coins=0):
    if session == 2 or session == 3:
        if params["language"] == "Hebrew":
            message = visual.TextStim(window,
                                      text=MIDDLE_SUMMARY_STR1_HE + (MIDDLE_SUMMARY_STR2Key_HE if params[
                                          "keyboardMode"] else MIDDLE_SUMMARY_STR2Joy_HE),
                                      units="norm",
                                      color=(255, 255, 255), languageStyle='RTL')
        else:
            message = visual.TextStim(window,
                                      text=MIDDLE_SUMMARY_STR1_EN + (MIDDLE_SUMMARY_STR2Key_EN if params[
                                          "keyboardMode"] else MIDDLE_SUMMARY_STR2Joy_EN),
                                      units="norm",
                                      color=(255, 255, 255), languageStyle='LTR')
        message.draw()

    else:
        screenNames = ["practice_start", "start_main_game"]
        image = visual.ImageStim(win=window, units="norm", opacity=1, size=(2, 2))
        if params["language"] == "Hebrew":
            image.image = "./img/InstructionsHebrew/" + screenNames[session] + ".jpeg"
        else:
            image.image = "./img/InstructionsEnglish/" + screenNames[session] + ".jpeg"
        image.draw()

    window.update()
    if params["keyboardMode"]:
        helpers.wait_for_space_no_df(window, io, df=df, mini_df=mini_df, summary_df=summary_df)
    else:
        helpers.wait_for_joystick_no_df(window, df=df, mini_df=mini_df, summary_df=summary_df)


def show_screen_post_simulation(window: visual.Window, params: dict, io, df=None, mini_df=None):
    image = visual.ImageStim(win=window, units="norm", opacity=1, size=(2, 2))
    image.image = ("./img/InstructionsHebrew/" if params[
                                                      "language"] == "Hebrew" else "./img/InstructionsEnglish/") + "SimulationRunEnd.jpeg"

    image.draw()
    window.update()

    if params["keyboardMode"]:
        helpers.wait_for_space_no_df(window, io, params, df, mini_df)
    else:
        helpers.wait_for_joystick_no_df(window, params, df, mini_df)


def show_wheel(window: visual.Window, params: dict, io=None):
    award_choice = random.choice([5, 6, 7])
    movie_path = f"./img/Wheels/{award_choice}_{params['language'][:3]}.mp4"
    movie = visual.MovieStim3(window, filename=movie_path, size=(2, 2), units="norm")

    while movie.status != FINISHED:
        movie.draw()
        window.flip()

    if params["keyboardMode"]:
        helpers.wait_for_space_no_df(window, io)
    else:
        helpers.wait_for_joystick_no_df(window)

    del movie
    return


def show_screen_post_match(window: visual.Window, params: dict, io, coins=0, df=None, mini_df=None):
    if params["language"] == "Hebrew":
        message = visual.TextStim(window,
                                  text=FINAL_SUMMARY_STR1_HE + f'{coins} ' + FINAL_SUMMARY_STR2_HE,
                                  units="norm",
                                  color=(255, 255, 255), languageStyle='RTL')
    else:
        message = visual.TextStim(window,
                                  text=FINAL_SUMMARY_STR1_EN + f'{coins} ' + FINAL_SUMMARY_STR2_EN,
                                  units="norm",
                                  color=(255, 255, 255), languageStyle='LTR')
    message.draw()
    window.update()
    if params["keyboardMode"]:
        helpers.wait_for_space_no_df(window, io, params, df, mini_df)
    else:
        helpers.wait_for_joystick_no_df(window, params, df, mini_df)


def play_sound(params, soundType: str, waitTime: float, dict_for_df: dict, Df: pandas.DataFrame, volume=1.):
    """
    The method plays a sound and sleeps through it, while recording data for the DF
    """

    soundToPlay = sound.Sound(SOUNDS[soundType], volume=volume)
    now = ptb.GetSecs()
    soundToPlay.play(when=now)
    startTime = time.time()
    while time.time() < startTime + waitTime:
        if params['saveFullDF']:
            dict_for_df["CurrentTime"] = round(time.time() - dict_for_df['StartTime'], 2)
            Df = pandas.concat([Df, pandas.DataFrame.from_records([dict_for_df])])
        core.wait(1 / 1000)
    soundToPlay.stop()
    return Df
