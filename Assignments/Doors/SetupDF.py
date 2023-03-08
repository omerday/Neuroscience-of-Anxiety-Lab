import pandas


def setup_data_frame(params: dict):
    params['headers'] = ['Time',
                         'ExpermientName',
                         'SubjectID',
                         'StartTime',
                         'CurrentTime',
                         'StepName',
                         'Session',  # 1 or 2
                         'Round',  # From 1 to 49 or 36
                         'RewardAmount',  # The amount offered for win
                         'PunishmentAmount',  # The amount offered for loss
                         'DistanceAtStart',  # Initial distance from the screen
                         'DistanceAtLock',  # Distance from the screen upon spacebar / 10 seconds
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
        params['headers'].append('EDG')

    Df = pandas.DataFrame(columns=params['headers'])
    return params, Df
