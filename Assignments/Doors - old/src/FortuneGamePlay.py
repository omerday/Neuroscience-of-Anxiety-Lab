import sys
sys.path.insert(1, './src')

import datetime,os
import subprocess as subp
from psychopy import visual
from Helper import waitUserSpace, tableWrite
from JoystickInput import JoystickInput
import time

def FortuneGamePlay(Df, win,params,SectionName,gameResult):
    Dict = {
        "Subject": params['subjectID'],
        "Session": params["Session"],
        "Version": params["Version"],
        "Section": SectionName,
        "SessionStartDateTime": datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S"),
    }

    img1 = visual.ImageStim(win=win, image="./img/changeme.jpg", units="pix", opacity=1,size=(1024, 768))
    img1.draw();win.flip()
    win.mouseVisible = False
    # waitUserSpace(Df, params)

    # Wait for User input.
    while (JoystickInput())['buttons_text'] == ' ':  # while presenting stimuli
        time.sleep(0.001)
        img1.draw();
        win.flip()
    while (JoystickInput())['buttons_text'] != ' ':  # while presenting stimuli
        time.sleep(0.001)

    win.mouseVisible = True
    win.close()
    if gameResult == 18:
        subp.check_call("runFortuneWheel18.bat "+os.getcwd(), shell=True)
        win = visual.Window(params['screenSize'], monitor="testMonitor", color="black", winType='pyglet')
        message = visual.TextStim(win,
                                  text="You have won $18.\n\nClick when you are ready to keep playing.",
                                  units='norm', wrapWidth=2)
    elif gameResult == 16:
        subp.check_call("runFortuneWheel16.bat "+os.getcwd(), shell=True)
        win = visual.Window(params['screenSize'], monitor="testMonitor", color="black", winType='pyglet')
        message = visual.TextStim(win,
                                  text="You have won $16.\n\nClick when you are ready to keep playing.",
                                  units='norm', wrapWidth=2)
    message.draw()
    win.flip()
    win.mouseVisible = False
    # waitUserSpace(Df, params)

    # Wait for User input.
    while (JoystickInput())['buttons_text'] == ' ':  # while presenting stimuli
        time.sleep(0.001)
        message.draw();
        win.flip()
    while (JoystickInput())['buttons_text'] != ' ':  # while presenting stimuli
        time.sleep(0.001)

    return tableWrite(Df, params,Dict),win
