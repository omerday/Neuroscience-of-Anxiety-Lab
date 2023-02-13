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
    :return:
    """
    isRandom = params['startingDistance'] == 'Random'
    isKeyboard = params['keyboardMode']
    imagePath = DOOR_IMAGE_PATH_PREFIX + f"p{punishment}r{reward}" + IMAGE_SUFFIX

    if isRandom:
        image = visual.ImageStim(win, image=imagePath,
                                 size=(params['screenSize'][0] * (1 + random.random()), params['screenSize'][1] * (1 + random.random())),
                                 units="pix", opacity=1)
    else:
        image = visual.ImageStim(win, image=imagePath,
                                 size=(params['screenSize'][0] * (1 + params['startingDistance'] / 100),
                                       params['screenSize'][1] * (1 + params['startingDistance'] / 100)),
                                units="pix", opacity=1)
    image.draw()
    win.update()
    return
