from psychopy import core, visual
import helpers

DOOR_IMAGE_PATH_PREFIX = './img/doors1/'
IMAGE_SUFFIX = '.jpg'


def setup_door(params, win, reward, punishment):
    isRandom = params['startingDistance'] == 'Random'
    isKeyboard = params['keyboardMode']
    imagePath = DOOR_IMAGE_PATH_PREFIX + f"p{punishment}r{reward}" + IMAGE_SUFFIX

    image = visual.ImageStim(win, image=imagePath, size=(params['screenSize'][0]*1.5, params['screenSize'][1]*1.5),
                             units="pix", opacity=1)
    image.draw()
    win.update()
    helpers.wait_for_space(win)
