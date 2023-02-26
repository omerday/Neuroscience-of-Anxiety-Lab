import time
from psychopy import core, event, visual
from psychopy.visual import ratingscale


def wait_for_space(window):
    """
    Helper method to wait for a Spacebar keypress and keep the window open until the window
    :param window:
    :return:
    """
    core.wait(1 / 120)
    c = event.getKeys()
    while 'space' not in c and 'escape' not in c:
        core.wait(1 / 120)
        c = event.getKeys()
    if 'escape' in c:
        window.close()
        core.quit()
    return


def wait_for_click(window):
    mouse = event.Mouse()
    mousePressed = mouse.getPressed()
    while mousePressed[0] != 1:
        mousePressed = mouse.getPressed()
    return


def display_vas(win, params, text, labels):
    """
    A helper method that displays VAS question (text object) and places a scale using psychopy.visual.ratingscale.
    The scale goes between two labels, and the answer (1-10_ is saved to Df, along with the response time
    :param win:
    :param params:
    :param text:
    :param labels:
    :return:
    """
    # TODO: Set up a dictionary that contains data for DataFrame
    # TODO: Add a DataFrame and write the answers to it

    scale = ratingscale.RatingScale(win,
                                    labels=labels,  # Labels at the edges of the scale
                                    scale=None, choices=None, low=0, high=100, precision=1, tickHeight=0, size=2,
                                    textSize=0.6, acceptText='Continue', showValue=False, showAccept=True,
                                    markerColor="Yellow")
    textItem = visual.TextStim(win, text=text, height=.12, units='norm', pos=[0, 0.3], wrapWidth=2)

    startTime = time.time()
    while scale.noResponse:
        scale.draw()
        textItem.draw()
        win.flip()
        get_keypress()
    endTime = time.time()
    return scale.getRating(), endTime - startTime


def get_keypress():
    keys = event.getKeys()
    if keys == ['q'] or keys == ['Q'] or keys == ['Esc']:
        core.quit()
