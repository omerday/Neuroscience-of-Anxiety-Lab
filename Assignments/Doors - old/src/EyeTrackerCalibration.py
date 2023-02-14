import sys
sys.path.insert(1, './src')

# Door Game Session Module.
def EyeTrackerCalibration(tracker):

    # run eyetracker calibration
    r = tracker.runSetupProcedure()

    # Check for and print any eye tracker events received...
    # tracker.setRecordingState(True)

    return tracker

