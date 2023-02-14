from psychopy import core, visual, event
import datetime, time
import pandas as pd
from psychopy.hardware import joystick
import pygame
from sys import exit
from JoystickInput import JoystickInput

def shutdown_key():
    core.quit()

def get_keypress(Df,params):
    keys = event.getKeys()
    if keys == ['q'] or keys == ['Q'] or keys == ['Esc']:
        # Write the output file.
        outFile = params['outFolder'] + '/' + str(params['subjectID']) + '_' + str(params['Session']) + '_' + \
                  str(params['Version']) + '_' + datetime.datetime.now().strftime("%m%d%Y_%H%M%S") + ".csv"

        print(outFile)
        Df.to_csv(outFile, sep=',', encoding='utf-8', index=False)

        print('Q pressed. Forced Exit.')
        core.quit()

def ResolutionIntialization(params,size_diff):
    width_bank = []
    height_bank = []
    width0 = params["screenSize"][0]
    height0 = params["screenSize"][1]
    # size_diff = 1/100
    if params['resolutionMode'] == False:
        for level in range(0,101):
            width = width0 * (0.0909 + level * size_diff)
            height = height0 * (0.0909 + level * size_diff)
            width_bank.append(width)
            height_bank.append(height)
    else:
        for level in range(0,101):
            width = width0 * (0.1 + pow(level,1.7) * size_diff*0.05)
            height = height0 * (0.1 + pow(level,1.7) * size_diff*0.05)
            width_bank.append(width)
            height_bank.append(height)
    params['width_bank'] = width_bank
    params['height_bank'] = height_bank

def triggerGo(port,params,r,p,e):
    if params['triggerSupport']:
        s = (e - 1) * 7 ** 2 + (int(p) - 1) * 7 + (int(r) - 1)
        port.setData(s)

def waitAnyKeys():
    # Wait for user types a space key.
    core.wait(1 / 120)
    c = ['']
    while (c[0] == ''):
        core.wait(1 / 120)
        c = event.waitKeys()  # read a character
        if c == ['q'] or c == ['Q'] or c == ['Esc']:
            print('Q pressed. Forced Exit.')
            core.quit()

def waitUserSpace(Df,params):
    # Wait for user types a space key.
    c = ['']
    while (c[0] != 'space'):
        core.wait(1 / 120)
        c = event.waitKeys()  # read a character

        if c == ['q'] or c == ['Q']:
            # Write the output file.
            outFile = params['outFolder'] + '/' + str(params['subjectID']) + '_' + str(params['Session']) + '_' + \
                      str(params['Version']) + '_' + datetime.datetime.now().strftime("%m%d%Y_%H%M%S") + ".csv"

            Df.to_csv(outFile, sep=',', encoding='utf-8', index=False)

            print('Q pressed. Forced Exit.')
            core.quit()

def waitUserSpaceAndC(Df,params):
    # Wait for user types a space key.
    c = ['']
    while (c[0] != 'space' and c[0] != 'c'):
        core.wait(1 / 120)
        c = event.waitKeys()  # read a character

        if c == ['q'] or c == ['Q']:
            # Write the output file.
            outFile = params['outFolder'] + '/' + str(params['subjectID']) + '_' + str(params['Session']) + '_' + \
                      str(params['Version']) + '_' + datetime.datetime.now().strftime("%m%d%Y_%H%M%S") + ".csv"

            Df.to_csv(outFile, sep=',', encoding='utf-8', index=False)

            print('Q pressed. Forced Exit.')
            core.quit()
    return c[0]

# Function to wait for any user input.
def waitUserInput(Df,img,win,params,mode):
    # if params['JoyStickSupport'] == False:
    #     event.waitKeys(maxWait=3)
    # # else:
    # if mode == 'glfw':
    #     joystick.backend = 'glfw'  # must match the Window
    # else:
    #     joystick.backend = 'pyglet'  # must match the Window
    # nJoys = joystick.getNumJoysticks()  # to check if we have any
    # if nJoys == 0:
    #     print("There is no available Joystick.")
    #     exit()
    # joy = joystick.Joystick(0)  # id must be <= nJoys - 1
    # startTime = time.time()
    #
    # count = 0
    # pygame.joystick.quit()
    # pygame.joystick.init()
    # while count < 3:  # while presenting stimuli
    #     # joy.getButton(0)
    #     # if sum(joy.getAllButtons())!=0:
    #     if joy.getButton(0)!=0:
    #         # print(joy.getAllButtons)
    #         # break
    #         count += 1
    #     if (time.time() - startTime) > 100:
    #         break
    #     img.draw();win.flip()
    #
    # get_keypress(Df, params)
    img.draw();win.flip()
    while (JoystickInput())['buttons_text'] == ' ':  # while presenting stimuli
        time.sleep(0.001)
        img.draw();
        win.flip()
    while (JoystickInput())['buttons_text'] != ' ':  # while presenting stimuli
        time.sleep(0.001)

# Question Session Module.
def Questionplay(Df, win, params, SectionName):
    Dict = {'ExperimentName': params['expName'],
            "Subject": params['subjectID'],
            "Session": params['Session'],
            "Version": params['Version'],
            "Section": SectionName,
            "SessionStartDateTime": datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S")}

    width = params["screenSize"][0]
    height = params["screenSize"][1]

    # Question (Won)
    Dict["Q_type"] = "Won"
    startTime = time.time()
    Dict["Q_score"], Dict["Q_RT"] = displayVAS(Df,params,win, "How many coins do you think you won?",
                                                       ['Won very few', 'Won very many'])
    Dict["Q_RT"] = (time.time() - startTime) * 1000
    Df = tableWrite(Df, params,Dict)  # Log the dict result on pandas dataFrame.

    # Question (Lost)
    Dict["Q_type"] = "Lost"
    Dict["SessionStartDateTime"] = datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S")
    startTime = time.time()
    Dict["Q_score"], Dict["Q_RT"] = displayVAS(Df,params,win, "How many coins do you think you lost?",
                                                       ['Lost very few', 'Lost very many'])
    Dict["Q_RT"] = (time.time() - startTime) * 1000
    Df = tableWrite(Df, params,Dict)  # Log the dict result on pandas dataFrame.

    # Question (Monster versus Coin)
    Dict["Q_type"] = "Before"
    Dict["SessionStartDateTime"] = datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S")
    startTime = time.time()
    Dict["Q_score"], Dict["Q_RT"] = displayVAS(Df,params,win, "Before the door opened, what did you think you would see?",
                                                       ['Monster', 'Coins'])
    Dict["Q_RT"] = (time.time() - startTime) * 1000
    Df = tableWrite(Df, params,Dict)  # Log the dict result on pandas dataFrame.

    # Question (Monster)
    Dict["Q_type"] = "Monster"
    Dict["SessionStartDateTime"] = datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S")
    startTime = time.time()
    Dict["Q_score"], Dict["Q_RT"] = displayVAS(Df,params,win, "How often did you see the monster when the door opened?",
                                                       ['Never', 'All the time'])
    Dict["Q_RT"] = (time.time() - startTime) * 1000
    Df = tableWrite(Df, params,Dict)  # Log the dict result on pandas dataFrame.

    # Question (Coins)
    Dict["Q_type"] = "Coins"
    Dict["SessionStartDateTime"] = datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S")
    startTime = time.time()
    Dict["Q_score"], Dict["Q_RT"] = displayVAS(Df,params,win,"How often did you win coins when the door opened?",
                                                       ['Never', 'All the time'])
    Dict["Q_RT"] = (time.time() - startTime) * 1000
    Df = tableWrite(Df, params,Dict)  # Log the dict result on pandas dataFrame.

    # Question (Performance)
    Dict["Q_type"] = "Performance"
    Dict["SessionStartDateTime"] = datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S")
    startTime = time.time()
    Dict["Q_score"], Dict["Q_RT"] = displayVAS(Df,params,win,"How do you feel about how well you’ve done so far?",
                                               ["I didn't do well","I did very well"])
    Dict["Q_RT"] = (time.time() - startTime) * 1000

    # Log the dict result on pandas dataFrame.
    Df = tableWrite(Df, params,Dict)

    # Ending Screen
    img1 = visual.ImageStim(win=win, image="./instruction/end_slide.jpg", units="pix", opacity=1, size=(width, height))
    # waitUserInput(Df,img1, win, params)
    img1.draw();
    win.flip()
    waitUserSpace(Df,params)

    return Df

# Door Game Session Module.


# Df,win,params,params['numTaskRun1'],port,"TaskRun1"
# SectionName = "TaskRun1"
# iterNum = params['numTaskRun1']


def tableWrite(df, params,dict):
    # Move data in Dict into Df.
    # Df = Df.append(pd.Series(dtype=float), ignore_index=True)  # Insert Empty Rows
    # Move data in Dict into Df.
    for key in params['Header']:
        if key not in dict.keys():
            dict[key] = ""
    df = df.append(dict,ignore_index=True)
    df.to_csv(params['outFile'], mode='a', sep=',', encoding='utf-8', index=False, header=False)

    # for key in Dict:
    #     Df[key].loc[len(Df) - 1] = Dict[key]  # FYI, len(Df)-1: means the last row of pandas dataframe.
    return df


def displayVAS(Df,params,win, text, labels):
    scale = visual.RatingScale(win,
                               labels=labels,  # End points
                               scale=None,  # Suppress default
                               # markerStart=50,
                               low=0, high=100, tickHeight=0, precision=1, size = 2,textSize = 0.6,
                               acceptText='Continue', showValue=False, showAccept=True,markerColor="Yellow")  # markerstart=50
    myItem = visual.TextStim(win, text=text, height=.12, units='norm',pos=[0,0.3], wrapWidth=2)

    # Show scale and measure the elapsed wall-clock time.
    startTime = time.time()
    while scale.noResponse:
        scale.draw()
        myItem.draw()
        win.flip()
        get_keypress(Df,params)
    endTime = time.time()
    win.flip()
    return scale.getRating(), endTime - startTime

def fadeInOutImage(win, image, duration, size):
    for i in range(60):
        opacity = 1 / 60 * (i + 1)
        img = visual.ImageStim(win=win, image=image, units="pix", opacity=opacity, size=size)
        img.draw();win.flip()
        core.wait(duration / 60)

    for i in range(60):
        opacity = 1 - 1 / 60 * (i + 1)
        img = visual.ImageStim(win=win, image=image, units="pix", opacity=opacity, size=size)
        img.draw();win.flip()
        core.wait(duration / 60)


def displayText(win, textString):
    message = visual.TextStim(win, text=textString)
    message.draw()
    win.flip()
