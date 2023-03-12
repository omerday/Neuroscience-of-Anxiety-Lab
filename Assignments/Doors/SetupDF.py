import pandas
import time


def setup_data_frame(params: dict):
    params['headers'] = ['Time',
                         'ExpermientName',
                         'SubjectID',
                         'StartTime',
                         'CurrentTime',
                         'StepName',
                         'Session',  # 1 or 2 in Task step, 1 to 3 in VAS step (Beginning-middle-end)
                         'Round',  # From 1 to 49 or 36
                         'RewardAmount',  # The amount offered for win
                         'PunishmentAmount',  # The amount offered for loss
                         'DistanceAtStart',  # Initial distance from the screen
                         'DistanceAtLock',  # Distance from the screen upon spacebar / 10 seconds
                         'CurrentDistance',
                         'MaxDistance',  # Maximal Distance from the Door
                         'MinDistance',  # Minimal Distance from the Door
                         'LockTime',  # When did the door lock
                         'DidDoorOpen',
                         'WinOrLose',
                         'DoorWaitTime',  # How long was the hold before opening the door
                         'TotalCoins',
                         'VASQuestionNumber',
                         'VASAnswer', ]

    if params['recordPhysio']:
        params['headers'].append('ECG')
        params['headers'].append('EMG')
        params['headers'].append('EDA')

    Df = pandas.DataFrame(columns=params['headers'])
    return params, Df


def create_dict_for_df(params: dict, **kwargs):
    dictLayout = {}
    for header in params['headers']:
        dictLayout[header] = None

    dictLayout['ExperimentName'] = 'Doors'
    dictLayout['SubjectID'] = params['subjectID']
    dictLayout['StartTime'] = time.time()
    for key, value in kwargs.items():
        if key in dictLayout.keys():
            dictLayout[key] = value
    return dictLayout
