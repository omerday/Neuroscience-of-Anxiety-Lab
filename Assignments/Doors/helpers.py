import time
from psychopy import core, event, visual
from psychopy.visual import ratingscale

#################################
# Helper method to wait for a Space key press
# And keep the window open until feedback
#################################

def wait_for_space(win):
    core.wait(1/120)
    c = event.getKeys()
    while 'space' not in c and 'escape' not in c:
        core.wait(1/120)
        c = event.getKeys()
    if 'escape' in c:
        win.close()
        core.quit()
    return


#################################
# Helper method that displays VAR question (text), and places it
# as a scale with Psychopy.visual.ratingscale. The Scale goes
# between the two lables, and the answer is saved to Df
#################################
def display_vas(win, params, text, labels):

    #TODO: Set up a dictionary that contains data for DataFrame
    #TODO: Add a DataFrame and write the answers to it

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
