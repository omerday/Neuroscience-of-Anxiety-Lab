import random
from psychopy import core, visual, event
import time
import pygame

DOOR_IMAGE_PATH_PREFIX = './img/doors1/'
OUTCOMES_IMAGE_PREFIX = './img/outcomes/'
IMAGE_SUFFIX = '.jpg'


def setup_door(window, params, punishment: int, reward: int):
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
    location = 0.6 - 0.1 * random.random() if isRandom else params[
                                                    'startingDistance'] / 100  # a variable for the relative location
    # of the subject from the door, should be 0-1
    imagePath = DOOR_IMAGE_PATH_PREFIX + f"p{punishment}r{reward}" + IMAGE_SUFFIX

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


def get_movement_input_keyboard(window, params, image: visual.ImageStim, location, end_time: time.time, io):
    """
    The method gets up/down key state and moves the screen accordingly.
    Note that for it to work, keyboard package needs to be loaded into psychopy (download the package files and place
    them in /Applications/PsychoPy.app/Contents/Resources/lib/python3.8, and if running on Mac - you need to run it as sudo.
    :param window:
    :param params:
    :param image:
    :param location:
    :param end_time:
    :param io:
    :return:
    """

    pygame.init()
    while time.time() < end_time:
        pygame.event.pump()
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                core.quit()

        if keys[pygame.K_UP]:
            if location < 1:
                image, location = move_screen(window, params, image, location, params['sensitivity'] * 0.5)
        elif keys[pygame.K_DOWN]:
            if location > 0:
                image, location = move_screen(window, params, image, location, params['sensitivity'] * (-0.5))
        elif keys[pygame.K_ESCAPE]:
            core.quit()
        elif keys[pygame.K_SPACE]:
            return location
        pygame.event.clear()
    return location


def get_movement_input_joystick(window, params, image: visual.ImageStim, location, end_time: time.time):
    pass


def start_door(window: visual.Window, params, image: visual.ImageStim, punishment: int, reward: int, location, io):
    start_time = time.time()
    end_time = start_time + 10
    key = event.getKeys()
    if params['keyboardMode']:
        location = get_movement_input_keyboard(window, params, image, location, end_time, io)
    else:
        # TODO: take joystick into consideration.
        pass
    total_time = time.time() - start_time
    random.seed(time.time() % 60)  # Seeding using the current second in order to have relatively random seed
    core.wait(2 + random.random() * 2)  # wait 2-4 seconds
    # Randomize door opening chance according to location:
    doorOpenChance = random.random()
    print(f'Door chance: {doorOpenChance}')
    isDoorOpening = doorOpenChance <= location
    print(f'isDoorOpening: {isDoorOpening}')
    if isDoorOpening:
        # Randomize the chances for p/r. If above 0.5 - reward. else - punishment.
        rewardChance = random.random()
        print(f'rewardChance: {rewardChance}')
        if rewardChance >= 0.5:
            image.setImage(OUTCOMES_IMAGE_PREFIX + f'{reward}_reward' + IMAGE_SUFFIX)
            image.setSize((2, 2))
            image.draw()
            window.update()
            core.wait(2)
            return reward, total_time
        else:
            image.setImage(OUTCOMES_IMAGE_PREFIX + f'{punishment}_punishment' + IMAGE_SUFFIX)
            image.setSize((2, 2))
            image.draw()
            window.update()
            core.wait(2)
            return -1 * punishment, total_time
    else:
        return 0, total_time
