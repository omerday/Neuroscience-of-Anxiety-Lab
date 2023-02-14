import random
from psychopy import core, visual
import helpers

DOOR_IMAGE_PATH_PREFIX = './img/doors1/'
IMAGE_SUFFIX = '.jpg'


def setup_door(params, win, reward, punishment):
    """
    Show door corresponding to the reward and punishment sent as arguments. Chooses the size in which it starts
    either randomly or fixed according to the parameters in order to be able to zoom out nicely.
    :param params: parameters from the main run
    :param win: psychopy windows object
    :param reward: reward (1-7)
    :param punishment: punishment (1-7)
    :return: image: the image object that will be used for movements
    :return: location: the relative location of the subject from the door, should be 1-100
    """
    isRandom = params['startingDistance'] == 'Random'
    location = random.random() if isRandom else params[
                                                    'startingDistance'] / 100  # a variable for the relative location of the subject from the door, should be 0-1
    imagePath = DOOR_IMAGE_PATH_PREFIX + f"p{punishment}r{reward}" + IMAGE_SUFFIX

    image = visual.ImageStim(win, image=imagePath,
                             size=(params['screenSize'][0] * (1 + location),
                                   params['screenSize'][1] * (1 + location)),
                             units="pix", opacity=1)

    image.draw()
    win.update()
    return image, location


def move_screen(win, params, image, location, units):
    """
    The method brings the image closer or further from the subject, according to the units of movement given.
    The units are converted from 1-100 to 0-1, and added to the location.
    :param win:
    :param params:
    :param image:
    :param location:
    :param units:
    :return: image: the updated image object
    :return: location: the updated location. Will be used to determine the chance of the door opening.
    """
    location = location + units / 100
    image.setSize((params['screenSize'][0] * (1 + location), params['screenSize'][1] * (1 + location)))
    image.draw()
    win.update()
    return image, location
