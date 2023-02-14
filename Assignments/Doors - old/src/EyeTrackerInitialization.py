import sys
sys.path.insert(1, './src')

from psychopy.iohub import launchHubServer
from psychopy.core import getTime, wait


# Door Game Session Module.
def EyeTrackerInitialization():

    iohub_config = {'eyetracker.hw.sr_research.eyelink.EyeTracker':
                        {'name': 'tracker',
                         'model_name': 'EYELINK 1000 DESKTOP',
                         'runtime_settings': {'sampling_rate': 500,
                                              'track_eyes': 'RIGHT'}
                         }
                    }
    io = launchHubServer(**iohub_config)

    # Get the eye tracker device.
    tracker = io.devices.tracker

    return tracker

