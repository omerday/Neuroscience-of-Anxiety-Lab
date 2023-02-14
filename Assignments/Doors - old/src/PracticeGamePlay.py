import sys
sys.path.insert(1, './src')

from psychopy import visual, event
from Helper import tableWrite,get_keypress,triggerGo,waitUserSpace,waitUserSpaceAndC
import random, datetime, glob, time
from ELIdxRecord import ELIdxRecord
from JoystickInput import JoystickInput
from WaitEyeGazed import WaitEyeGazed
from EyeTrackerCalibration import EyeTrackerCalibration
from psychopy.iohub import launchHubServer
import pylink,time

# Debuging
# PracticeGamePlay(Df, win, params, params['numPractice'], port, "Practice")
# iterNum = params['numPractice']; SectionName = "Practice"

def newPoint(n,center,ratio):
    return int((n-center) * ratio + center)

# Door Game Session Module.
def PracticeGamePlay(Df, DfTR,win, params, iterNum, port,SectionName):

    # Eyetracker start recording
    params["idxTR"] = 0
    if params['EyeTrackerSupport']:

        message = visual.TextStim(win,
                                  text="Eyetracker Calibration will start.  \n\nPress the spacebar when you are ready.",
                                  units='norm', wrapWidth=2)
        message.draw();
        win.flip();
        waitUserSpace(Df, params)

        iohub_config = {'eyetracker.hw.sr_research.eyelink.EyeTracker':
                            {'name': 'tracker',
                             'model_name': 'EYELINK 1000 DESKTOP',
                             'runtime_settings': {'sampling_rate': 500,
                                                  'track_eyes': 'LEFT'}
                             }
                        }
        # Start new ioHub server.
        import psychopy.iohub.client

        try:
            io = launchHubServer(**iohub_config)
        except:
            q = psychopy.iohub.client.ioHubConnection.getActiveConnection().quit()
            io = launchHubServer(**iohub_config)

        # Get the eye tracker device.
        tracker = io.devices.tracker

        tracker.sendCommand("screen_pixel_coords = 0 0 %d %d" % (params['screenSize'][0] - 1, params['screenSize'][1] - 1))

        # save screen resolution in EDF data, so Data Viewer can correctly load experimental graphics
        # see Data Viewer User Manual, Section 7: Protocol for EyeLink Data to Viewer Integration
        tracker.sendMessage("DISPLAY_COORDS = 0 0 %d %d" % (params['screenSize'][0] - 1, params['screenSize'][1] - 1))

        # Eyetracker Calibration.
        c = 'c'
        while c != 'space':
            tracker = EyeTrackerCalibration(tracker)
            win.close()
            win = visual.Window(params['screenSize'], monitor="testMonitor", color="black", winType='pyglet')
            message = visual.TextStim(win,
                                      text="Calibration is completed.  Press the spacebar when you are ready to keep playing.\n Press 'c' to do calibration again.",
                                      units='norm', wrapWidth=2)
            message.draw();
            win.flip();
            c = waitUserSpaceAndC(Df, params)
        win.close()

        # Eyetracker start recording
        tracker.setRecordingState(True)
        ELstartTime = time.time()

    win.close()
    win = visual.Window(params['screenSize'], monitor="testMonitor", color="black", winType='pyglet')
    win.mouseVisible = False

    width = params["screenSize"][0]
    height = params["screenSize"][1]

    # Start Section Display
    img1 = visual.ImageStim(win=win, image="./instruction/practice_start.jpg", units="pix", opacity=1,size=(width, height))
    # waitUserInput(Df,img1, win, params,'glfw')
    img1.draw();win.flip()

    # Wait for User input.
    while (JoystickInput())['buttons_text'] == ' ':  # while presenting stimuli
        time.sleep(0.001)
        img1.draw();
        win.flip()
    while (JoystickInput())['buttons_text'] != ' ':  # while presenting stimuli
        time.sleep(0.001)

    # Read Door Open Chance file provided by Rany.
    imgList = glob.glob("./img/practice/*_door.jpg")

    # Joystick Initialization
    if JoystickInput() == -1:
        print("There is no available Joystick.")
        exit()


        # Eyetracker label record
        # tracker.sendMessage('TRIAL_RESULT 0') # # EDF labeling (end)
    if params['EyeTrackerSupport']:
        DfTR = ELIdxRecord(DfTR, params, SectionName, time.time()-ELstartTime,"", "After Calibration Before Door Practice Game","","")
        tracker.sendMessage('TRIAL_RESULT 0')

    # joy = joystick.Joystick(0)  # id must be <= nJoys - 1
    aoiTimeStart = time.time() * 1000
    for i in range(iterNum):

        # EDF labeling (start)
        if params['EyeTrackerSupport']:
            tracker.sendMessage('TRIALID %d' % params["idxTR"])
            ELstartTime = time.time()

        Dict = {
            "ExperimentName" : params['expName'],
            "Subject" : params['subjectID'],
            "Session" : params["Session"],
            "Version" : params["Version"],
            "Section" : SectionName,
            "SessionStartDateTime" : datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S")
        }

        # Pick up random image.
        randN = random.randint(0, len(imgList) - 1)
        imgFile = imgList[randN]

        # Display the image.
        c = ['']
        level = Dict["Distance_start"] = params["DistanceStart"]
        startTime = time.time()

        Dict["Distance_max"] = Dict["Distance_min"] = params["DistanceStart"]
        Dict["Distance_lock"] = 0
        MaxTime = params['DistanceLockWaitTime'] * 1000

        # Initial screen
        width = params['width_bank'][level]
        height = params['height_bank'][level]
        img1 = visual.ImageStim(win=win, image=imgFile, units="pix", opacity=1, size=(width, height))
        # img1.draw();

        if params['EyeTrackerSupport']:
            position = (0,0)
            circle = visual.Circle(win=win, units="pix", fillColor='black', lineColor='white', edges=1000, pos=position,
                                   radius=5)

            # tracker.sendMessage('!V IMGLOAD CENTER %s %d %d' % (imgFile, 1024/2, 768 / 2))

        triggerGo(port, params, 1, 1, 1)  # Door onset (conflict)
        win.flip()

        count = 0
        joy = JoystickInput()

        while count < 4:  # while presenting stimuli
            # If waiting time is longer than 10 sec, exit this loop.
            Dict["DoorAction_RT"] = (time.time() - startTime) * 1000
            if Dict["DoorAction_RT"] > MaxTime:
                c[0] = "timeisUp"
                break
            # if (sum(joy.getAllButtons()) != 0):
            # if joy.getButton(0)!=0:
            if joy['buttons_text'] != ' ':
                count += 1

            if count >= 4:
                Dict["Distance_lock"] = 1
                break

            joy = JoystickInput()
            joyUserInput = joy['y']

            changed = True
            if joyUserInput < -0.5 and level < 100:
                level += 2
                level = min(100,level)
            elif joyUserInput < -0.1-params['sensitivity']*0.1 and level < 100:
                level += 1
                level = min(100,level)
            elif joyUserInput > 0.5 and level > 0:
                level -= 2
                level = max(0,level)
            elif joyUserInput > 0.1+params['sensitivity']*0.1 and level > 0:
                level -= 1
                level = max(0, level)
            else:
                changed = False
            get_keypress(Df,params)
            width = params['width_bank'][level]
            height = params['height_bank'][level]

            # preInput = joyUserInput
            Dict["Distance_max"] = max(Dict["Distance_max"], level)
            Dict["Distance_min"] = min(Dict["Distance_min"], level)

            img1.size = (width, height)
            img1.draw()

            if params['EyeTrackerSupport']:

                positionTmp = position
                position = tracker.getPosition()
                if position is None:
                    position = positionTmp

                circle.pos = position
                if params['eyeTrackCircle']:
                    circle.draw()

                aoiTimeEnd = time.time() * 1000
                if changed == True:
                    tracker.sendMessage('!V IAREA %d %d RECTANGLE %d %d %d %d %d %s' % (int(aoiTimeEnd-aoiTimeStart),0,
                                                                                        1, 512 - width * 105 / 1024,
                                                                                        390 - height * 160 / 768,
                                                                                        512 + width * 105 / 1024,
                                                                                        390 + height * 200 / 768, 'DOOR'))

                    aoiTimeStart = aoiTimeEnd

            win.flip()

        if params['EyeTrackerSupport']:
            tracker.sendMessage('TRIAL_RESULT 0')
            DfTR = ELIdxRecord(DfTR, params,SectionName,time.time()-ELstartTime,i, "Playing Door Game (Before lock).","","")
            tracker.sendMessage('TRIALID %d' % params["idxTR"])
            tracker.sendMessage('!V IMGLOAD CENTER %s %d %d %d %d' % (imgFile, 1024/2, 768 / 2, width, height))
            tracker.sendMessage('!V IAREA RECTANGLE %d %d %d %d %d %s' % (1, 512-width*105/1024,
                                                                                390-height*160/768,
                                                                                512+width*105/1024,
                                                                                390+height*200/768,
                                                                                'DOOR'))
            ELstartTime = time.time()


        triggerGo(port, params, 1, 1, 2)  # Joystick lock (start anticipation)
        Dict["DistanceFromDoor_SubTrial"] = level

        # Door Anticipation time
        Dict["Door_anticipation_time"] = random.uniform(2, 4) * 1000
        time.sleep(Dict["Door_anticipation_time"] / 1000)

        if params['EyeTrackerSupport']:
            tracker.sendMessage('TRIAL_RESULT 0')
            DfTR = ELIdxRecord(DfTR, params,SectionName,time.time()-ELstartTime,i, "After lock: Door Anticipation Time.","","")
            tracker.sendMessage('TRIALID %d' % params["idxTR"])
            tracker.sendMessage('!V IMGLOAD CENTER %s %d %d %d %d' % ('./img/practice/combined.jpg', 1024 / 2, 768 / 2, width, height))
            tracker.sendMessage('!V IAREA RECTANGLE %d %d %d %d %d %s' % (1, 512-width*50/1024,
                                                                                390-height*40/768,
                                                                                512+width*50/1024,
                                                                                390+height*50/768,
                                                                                'Reward (Question mark)'))
            ELstartTime = time.time()

        awardImg = "./img/practice/practice_outcome.jpg"
        img2 = visual.ImageStim(win=win, image=awardImg, units="pix", opacity=1, pos=[0, -height * 0.028],
                                size=(width* 0.235, height* 0.464))
        img1.draw();img2.draw();win.flip()

        event.waitKeys(maxWait=2)
        if params['EyeTrackerSupport']:
            tracker.sendMessage('TRIAL_RESULT 0')
            DfTR = ELIdxRecord(DfTR, params,SectionName,time.time()-ELstartTime,i, "Reward screen displayed.","","")
            tracker.sendMessage('TRIALID %d' % params["idxTR"])
            ELstartTime = time.time()

        # ITI duration
        if params['EyeTrackerSupport']:
            startTime = time.time()
            width = params["screenSize"][0]
            height = params["screenSize"][1]
            tracker.sendMessage('!V IMGLOAD CENTER %s %d %d' % ("./img/ITI_fixation.jpg", width/2, height/2))
            tracker.sendMessage('!V IAREA RECTANGLE %d %d %d %d %d %s' % (
            1, int(335 * width / 1024), int(217 * height / 768), int(689 * width / 1024), int(561 * height / 768),
            'fixation treasure'))

            WaitEyeGazed(win, params, tracker,'eyeTrackCircle')
            Dict["ITI_duration"] = time.time() - startTime

        else:
            width = params["screenSize"][0]
            height = params["screenSize"][1]
            img1 = visual.ImageStim(win=win, image="./img/iti.jpg", units="pix", opacity=1, size=(width, height))
            img1.draw();win.flip();
            Dict["ITI_duration"] = random.uniform(1.5, 3.5) * 1000
            time.sleep(Dict["ITI_duration"] / 1000)

        if params['EyeTrackerSupport']:
            tracker.sendMessage('TRIAL_RESULT 0')
            DfTR = ELIdxRecord(DfTR, params,SectionName,time.time()-ELstartTime,i, "ITI screen displayed.","","")

        Df = tableWrite(Df, params,Dict)  # Log the dict result on pandas dataFrame.


    # Eyetracker finish recording
    if params['EyeTrackerSupport']:
        # Eyetracker stop recording
        tracker.setRecordingState(False)

        # open a connection to the tracker and download the result file.
        trackerIO = pylink.EyeLink('100.1.1.1')
        trackerIO.receiveDataFile("et_data.EDF", params[SectionName])
        # tracker._eyelink.receiveDataFile("et_data.EDF", params[SectionName])
        # Stop the ioHub Server
        io.quit()
        trackerIO.close()

    win.mouseVisible = True
    return Df,DfTR,win

