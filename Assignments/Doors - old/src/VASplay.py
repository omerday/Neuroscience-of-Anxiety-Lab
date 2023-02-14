import sys
sys.path.insert(1, './src')

from psychopy import visual
from Helper import waitUserSpace,displayVAS,tableWrite
import datetime, time

# VAS Session Module.
def VASplay(Df, win, params, SectionName):
    # VAS Initialization.
    Dict = {'ExperimentName': params['expName'],
            "Subject": params['subjectID'],
            "Session": params['Session'],
            "Version": params['Version'],
            "Section": SectionName,
            "VAS_type": "Anxiety",
            "SessionStartDateTime": datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S")}

    # VAS Start Screen
    message = visual.TextStim(win, text="Before we continue, please answer a few questions. \n\n Press the spacebar to continue.",units='norm', wrapWidth=3)
    message.draw();win.flip()
    # waitUserInput(Df,message, win, params)
    waitUserSpace(Df,params)
    # event.waitKeys(maxWait=3)

    # VAS (Anxiety)
    startTime = time.time()
    Dict["VAS_score"], Dict["VAS_RT"] = displayVAS(Df,params,win, "How anxious do you feel right now?",
                                                       ['Not anxious', 'Very anxious'])
    Dict["VAS_RT"] = (time.time() - startTime) * 1000
    Df = tableWrite(Df, params, Dict)  # Log the dict result on pandas dataFrame.

    # VAS (Avoidance)
    Dict["VAS_type"] = "Avoidance"
    Dict["SessionStartDateTime"] = datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S")
    startTime = time.time()
    Dict["VAS_score"], Dict["VAS_RT"] = displayVAS(Df,params,win, "How much do you feel like taking part in the task?",
                                                       ['Not at all', 'Very much'])
    Dict["VAS_RT"] = (time.time() - startTime) * 1000
    Df = tableWrite(Df, params,Dict)  # Log the dict result on pandas dataFrame.

    # VAS (Tired)
    Dict["VAS_type"] = "Tired"
    Dict["SessionStartDateTime"] = datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S")
    startTime = time.time()
    Dict["VAS_score"], Dict["VAS_RT"] = displayVAS(Df,params,win, "How tired are you right now?",
                                                       ['Not at all tired', 'Very tired'])
    Dict["VAS_RT"] = (time.time() - startTime) * 1000
    Df = tableWrite(Df, params,Dict)  # Log the dict result on pandas dataFrame.

    # VAS (Mood)
    Dict["VAS_type"] = "Mood"
    Dict["SessionStartDateTime"] = datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S")
    startTime = time.time()
    Dict["VAS_score"], Dict["VAS_RT"] = displayVAS(Df,params,win,
                                                       "Think about your mood right now. \nHow would you describe it?",
                                                       ['Worst mood ever', 'Best mood ever'])
    Dict["VAS_RT"] = (time.time() - startTime) * 1000
    return tableWrite(Df, params,Dict)  # Log the dict result on pandas dataFrame.
