import sys
sys.path.insert(1, './src')

from psychopy import visual, event,core
import time

# Door Game Session Module.
def WaitEyeGazed(win, params,tracker,circleCheck):
    img = visual.ImageStim(win=win, image="./img/ITI_fixation.jpg", units="pix", opacity=1,
                           size=(params['screenSize'][0], params['screenSize'][1]))

    c = event.getKeys()
    circle = visual.Circle(win=win, units="pix", fillColor='black', lineColor='white', edges=1000, pos=(0,0),
                           radius=10)
    img.draw()
    if circleCheck:
        circle.draw()
    win.flip()
    while (c != ['space']):
        core.wait(1 / 120)
        c = event.getKeys()
        position = tracker.getPosition()
        if position is None:
            continue
        # for i in range(2):
        #     position[i] *= 1
        # if c == ['r']:
        #     print(position)

        # Thresholding
        position[0] = params['screenSize'][0] if position[0]>params['screenSize'][0] else position[0]
        position[0] = -1*params['screenSize'][0] if position[0] < -1 * params['screenSize'][0] else position[0]
        position[1] = params['screenSize'][1] if position[1]>params['screenSize'][1] else position[1]
        position[1] = -1*params['screenSize'][1] if position[1] < -1 * params['screenSize'][1] else position[1]

        startTime = time.time()
        gazeTime = 0
        while abs(position[0])<80 and abs(position[1]) <80:
            gazeTime = time.time() - startTime
            positionTmp = position
            position = tracker.getPosition()

            if position is None:
                position = positionTmp
                # continue

            circle.pos = position
            img.draw()
            if circleCheck:
                circle.draw()
            win.flip()

        img.draw()
        circle.pos = position
        if circleCheck:
            circle.draw()
        win.flip()


        if gazeTime > 0.5:
            break