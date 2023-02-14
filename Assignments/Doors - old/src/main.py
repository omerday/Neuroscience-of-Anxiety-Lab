# Python3-based package
"""
DoorTaskPlayGame.py

DoorTask Game Main Driver File.

Created on Fri July 24 15:04:19 2020

Bug: not working with AMD Radeon GPU devices. (worked with NVIDA)

@author: Kyunghun Lee
- Created July/24/20 by KL
- Updated 09/3/2020 Tue by KL (Trigger)
- Updated 09/15/2020 Tue by KL (Major Updates)
- Updated 4/21/2021 Wed by KL (Eyetracker update - major updates)
- Updated Fri, Oct  8, 2021  1:42:55 PM by KL (Reward/punishment score display on AOIs)
- Updated Fri, Mar 11, 2022  4:13:50 PM by KL (Instruction updated)
- Save result when exit 10/26/2020 Mon by KL
- Dynamic AOI updated Tue, Apr 12, 2022  3:21:26 PM by Lucrezia
- Fortune Wheel updated Tue, May 31, 2022 11:29:44 AM by Kyunghun

"""

# Import developer-defined functions
import sys,os
sys.path.insert(1, '')
import datetime
import pandas as pd
from psychopy import visual,core,event
from Helper import Questionplay,waitUserSpace
from Helper import waitUserInput, waitAnyKeys,ResolutionIntialization

from userInputPlay import userInputPlay
from VASplay import VASplay
from InstructionPlay import InstructionPlay
from PracticeGamePlay import PracticeGamePlay
#from DoorGamePlay import DoorGamePlay
from FortuneGamePlay import FortuneGamePlay
from psychopy import parallel
from psychopy import prefs
import subprocess as subp

def shutdown_key():
    core.quit()

# Receive User input from User input window.
userInputBank = userInpxutPlay()

# Declare primary task parameters.
params = {
# Declare stimulus and response parameters
    'expName' : "Doors_AA_v8.py", # The name of the experiment
    'subjectID' : userInputBank[0],      # Subject ID
    'DistanceStart' : 50,
    'DistanceLockWaitTime' : 10, # Distance lock wait time.
    'Session' : userInputBank[1], # Session ID
    'Version' : userInputBank[2], # Version
    'numPractice' : userInputBank[3], # The number of Trials in Practice.
    'numTaskRun1': userInputBank[4],  # The number of Trials in TaskRun1.
    'numTaskRun2': userInputBank[5],  # The number of Trials in TaskRun2.
    'numTaskRun3': userInputBank[6],  # The number of Trials in TaskRun2.
    'JoyStickSupport' : True, # Check if joystick option is checked or not.
    'triggerSupport': userInputBank[7],  # Check if joystick option is checked or not.
    'EyeTrackerSupport': userInputBank[8],
    'FullScreen': userInputBank[9],
    'sensitivity': userInputBank[10],
    'soundMode' : userInputBank[11],
    # 'eyeTrackCircle': userInputBank[11],
    'eyeTrackCircle': True,
    'portAddress': int("0xE050", 16), # Port Address
    'imageDir': './img/doors1/',    # directory containing DOOR image stimuli (default value)
    'imageSuffix': '*.jpg',   # DOOR image extension.
    'totalRewardThreshold' : 20, # The total number of coin to get Extra $10 reward.

# declare output file location
    'outFolder': './output', # the location of output file.

# declare display parameters
    'screenSize' : (1024,768),
    'volume' : 0.8,
    'resolutionMode' : True,
    'subTrialCounter': 0,
    'idxTR': 0,
    'idxImg': 0,
}

# Audio library configuration.
if params['soundMode'] == 'PTB':
    prefs.hardware['audioLib'] = ['PTB']
else:
    prefs.hardware['audioLib'] = ['pygame', 'pyo', 'sounddevice', 'PTB']


# Define Output file names.
timeLabel = datetime.datetime.now().strftime("%m%d%Y_%H%M%S")
params['outFile'] = params['outFolder'] + '/' + str(params['subjectID']) + '_' + str(params['Session']) + '_' + \
          str(params['Version']) + '_' +  timeLabel + ".csv"
params['outFileTrackerLog'] = params['outFolder'] + '/' + str(params['subjectID']) + '_' + str(params['Session']) + '_' + \
          str(params['Version']) + '_' +  timeLabel + "TR.csv"
params['Practice'] =  params['outFolder'] + '/' +str(params['subjectID']) + '_' + str(params['Session']) + '_' + \
          str(params['Version']) + '_' +  timeLabel + "PR.EDF"
params['TaskRun1'] = params['outFolder'] + '/' +str(params['subjectID']) + '_' + str(params['Session']) + '_' + \
          str(params['Version']) + '_' +  timeLabel + "TR1.EDF"
params['TaskRun2'] = params['outFolder'] + '/' +str(params['subjectID']) + '_' + str(params['Session']) + '_' + \
          str(params['Version']) + '_' +  timeLabel + "TR2.EDF"
params['TaskRun3'] = params['outFolder'] + '/' +str(params['subjectID']) + '_' + str(params['Session']) + '_' + \
          str(params['Version']) + '_' +  timeLabel + "TR3.EDF"

prefs.general['fullscr'] = params['FullScreen']

# Global Exit
event.globalKeys.add(key='q', func=os._exit, func_args=[1], func_kwargs=None)

if userInputBank[3]!= 1:
    params['imageDir'] = './img/doors2/'

## Setup Psychopy Window.
win = visual.Window(params['screenSize'], monitor="testMonitor",color="black",winType='pyglet')
img = visual.ImageStim(win=win, image="./img/ITI_fixation.jpg", units="pix", opacity=1, size=(params[ 'screenSize'][0], params['screenSize'][1]))

# Trigger Initialization
port = 0
if params['triggerSupport']:
    port = parallel.ParallelPort(address=params['portAddress'])
    port.setData(0) # initialize to all zeroscv

# ====================== #
# ==== Title Screen ==== #
# ====================== #
img1 = visual.ImageStim(win=win,image="./img/title.jpg",units="pix",size=params['screenSize'],opacity=1) #
win.mouseVisible = False
img1.draw();win.flip();
waitAnyKeys()

# ======================== #
# Dataframe Initialization #
# ======================== #
params['Header'] = ["ExperimentName","SessionStartDateTime","Subject","Session","Version","Section","Subtrial",
          "DistanceFromDoor_SubTrial","Distance_lock","Distance_start","Distance_min","Distance_max",
          "Door_anticipation_time","Door_opened","Door_outcome","Reward_magnitude","Punishment_magnitude",
          "DoorAction_RT","ITI_duration","Total_coins","VAS_type","VAS_score","VAS_RT","Q_type","Q_score","Q_RT"]
params['HeaderTR'] = ["Index", "subjectID", "Session", "Version", "Section", "Subtrial", "Event", "Reward", "Punishment",
            "Duration(ms)"]

# Pandas dataframe Initialization
Df = pd.DataFrame(columns=params['Header'])
if params['EyeTrackerSupport']:
    DfTR = pd.DataFrame(columns=params['HeaderTR'])
else:
    DfTR = ""

# Make Empty output files.
Df.to_csv(params['outFile'], sep=',', encoding='utf-8', index=False)
if params['EyeTrackerSupport']:
    DfTR.to_csv(params['outFileTrackerLog'], sep=',', encoding='utf-8', index=False)

# ====================== #
# ======== VAS pre ========= #
# ====================== #
win.mouseVisible = True
Df = VASplay(Df,win,params,"VAS pre")
win.mouseVisible = False

# ====================== #
# ===== Instruction ==== #
# ====================== #
Df = InstructionPlay(Df,win,params)

# ========================================== #
# ==== Screen Resolution Initialization ==== #
# ========================================== #
ResolutionIntialization(params,size_diff=1/65)

# ========================================== #
# ==== Eyetracker Initialization =========== #
# ========================================== #
tracker = ""
# if params['EyeTrackerSupport']:

# ====================== #
# ===== Practice ======= #
# ====================== #
win.mouseVisible = False
iterNum = params['numPractice']
SectionName = "Practice"

Df,DfTR,win = PracticeGamePlay(Df, DfTR,win, params, iterNum, port,SectionName)
win.mouseVisible = True

# ====================== #
# ===Fortune Wheel1 ==== #
# ====================== #
# win.close()
Df,win = FortuneGamePlay(Df, win,params,"Fortune Wheel 1",18)
# win = visual.Window(params['screenSize'], monitor="testMonitor",color="black",winType='pyglet')

# ====================== #
# ===== TaskRun1 ======= #
# ====================== #
win.mouseVisible = False
Df,DfTR,win = DoorGamePlay(Df,DfTR,win,params,params['numTaskRun1'],port,"TaskRun1")
win.mouseVisible = True

# ====================== #
# ======== VAS 1 ========= #
# ====================== #
win.mouseVisible = True
# message = visual.TextStim(win, text="Let's rest for a bit. Click when you are ready to keep playing.", units='norm', wrapWidth=2)
message = visual.TextStim(win, text="Let's rest for a bit.  Press the spacebar when you are ready to keep playing.", units='norm', wrapWidth=2)
message.draw();win.flip();
waitUserSpace(Df,params)
Df = VASplay(Df,win,params,"VAS 1")
win.mouseVisible = False

# ====================== #
# ======== Text Slide ========= #
# ====================== #
# message = visual.TextStim(win, text="Click when you are ready to continue the game.", units='norm', wrapWidth=3)
# message.draw();
win.mouseVisible = False
img1 = visual.ImageStim(win=win,image="./img/after_VAS2.jpg",units="pix",size=params['screenSize'],opacity=1) #
waitUserInput(Df,img1, win, params,'pyglet')
win.flip();

# ====================== #
# ===Fortune Wheel2 ==== #
# ====================== #
# win.close()
Df,win = FortuneGamePlay(Df, win,params,"Fortune Wheel 2",16)
# win = visual.Window(params['screenSize'], monitor="testMonitor",color="black",winType='pyglet')

# ====================== #
# ===== TaskRun2 ======= #
# ====================== #
Df,DfTR,win = DoorGamePlay(Df,DfTR,win,params,params['numTaskRun2'],port,"TaskRun2")

# ====================== #
# ======== VAS mid ========= #
# ====================== #
win.mouseVisible = True
message = visual.TextStim(win, text="Let's rest for a bit.  Press the spacebar when you are ready to keep playing.", units='norm', wrapWidth=2)
message.draw();win.flip();
waitUserSpace(Df,params)
Df = VASplay(Df,win,params,"VAS mid")
win.mouseVisible = False

# ====================== #
# ======== Text Slide ========= #
# ====================== #
img1 = visual.ImageStim(win=win,image="./img/after_VAS2.jpg",units="pix",size=params['screenSize'],opacity=1) #
waitUserInput(Df,img1, win, params,'pyglet')
win.flip();

# ====================== #
# ===Fortune Wheel3 ==== #
# ====================== #
# win.close()
Df,win = FortuneGamePlay(Df, win,params,"Fortune Wheel 3",16)
# win = visual.Window(params['screenSize'], monitor="testMonitor",color="black",winType='pyglet')

# ====================== #
# ===== TaskRun3 ======= #
# ====================== #
win.mouseVisible = False
Df,DfTR,win = DoorGamePlay(Df,DfTR,win,params,params['numTaskRun3'],port,"TaskRun3")
win.mouseVisible = True

# ====================== #
# ======== VAS post ========= #
# ====================== #
win.mouseVisible = True
# message = visual.TextStim(win, text="Let's rest for a bit.  when you are ready to keep playing.", units='norm', wrapWidth=2)
message = visual.TextStim(win, text="Let's rest for a bit.  Press the spacebar when you are ready to keep playing.", units='norm', wrapWidth=2)
message.draw();win.flip();
waitUserSpace(Df,params)
Df = VASplay(Df,win,params,"VAS post")
win.mouseVisible = False

# ====================== #
# ======== Question ========= #
# ====================== #
win.mouseVisible = True
Df = Questionplay(Df, win, params, "Question")

Df.to_csv(params['outFile'], sep=',', encoding='utf-8', index=False)
if params['EyeTrackerSupport']:
    DfTR.to_csv(params['outFileTrackerLog'], sep=',', encoding='utf-8', index=False)

# Close the psychopy window.
win.close()
