from psychopy import core, visual, event
import datetime, time
import pandas as pd
from psychopy.hardware import joystick
#import pygame
from sys import exit
from JoystickInput import JoystickInput
from Helper import waitUserSpace,displayVAS,tableWrite

# Question Session Module.
def QuestionPlay(Df, win, params, SectionName):
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
    tableWrite(Df, params,Dict)  # Log the dict result on pandas dataFrame.

    # Question (Lost)
    Dict["Q_type"] = "Lost"
    Dict["SessionStartDateTime"] = datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S")
    startTime = time.time()
    Dict["Q_score"], Dict["Q_RT"] = displayVAS(Df,params,win, "How many coins do you think you lost?",
                                                       ['Lost very few', 'Lost very many'])
    Dict["Q_RT"] = (time.time() - startTime) * 1000
    tableWrite(Df, params,Dict)  # Log the dict result on pandas dataFrame.

    # Question (Monster versus Coin)
    Dict["Q_type"] = "Before"
    Dict["SessionStartDateTime"] = datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S")
    startTime = time.time()
    Dict["Q_score"], Dict["Q_RT"] = displayVAS(Df,params,win, "Before the door opened, what did you think you would see?",
                                                       ['Monster', 'Coins'])
    Dict["Q_RT"] = (time.time() - startTime) * 1000
    tableWrite(Df, params,Dict)  # Log the dict result on pandas dataFrame.

    # Question (Monster)
    Dict["Q_type"] = "Monster"
    Dict["SessionStartDateTime"] = datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S")
    startTime = time.time()
    Dict["Q_score"], Dict["Q_RT"] = displayVAS(Df,params,win, "How often did you see the monster when the door opened?",
                                                       ['Never', 'All the time'])
    Dict["Q_RT"] = (time.time() - startTime) * 1000
    tableWrite(Df, params,Dict)  # Log the dict result on pandas dataFrame.

    # Question (Coins)
    Dict["Q_type"] = "Coins"
    Dict["SessionStartDateTime"] = datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S")
    startTime = time.time()
    Dict["Q_score"], Dict["Q_RT"] = displayVAS(Df,params,win,"How often did you win coins when the door opened?",
                                                       ['Never', 'All the time'])
    Dict["Q_RT"] = (time.time() - startTime) * 1000
    tableWrite(Df, params,Dict)  # Log the dict result on pandas dataFrame.

    # Question (Performance)
    Dict["Q_type"] = "Performance"
    Dict["SessionStartDateTime"] = datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S")
    startTime = time.time()
    Dict["Q_score"], Dict["Q_RT"] = displayVAS(Df,params,win,"How do you feel about how well you’ve done so far?",
                                               ["I didn't do well","I did very well"])
    Dict["Q_RT"] = (time.time() - startTime) * 1000

    # Log the dict result on pandas dataFrame.
    tableWrite(Df, params,Dict)

    # Ending Screen
    img1 = visual.ImageStim(win=win, image="./instruction/end_slide.jpg", units="pix", opacity=1, size=(width, height))
    # waitUserInput(Df,img1, win, params)
    img1.draw();
    win.flip()
    waitUserSpace(Df,params)