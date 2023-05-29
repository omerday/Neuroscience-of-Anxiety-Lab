import pandas
import time
import datetime
# import bioread
import matplotlib
# import seaborn as sns


# TODO: Change VAS Type
def setup_data_frame(params: dict):
    params['headers'] = ['Time',
                         'ExpermientName',
                         'SubjectID',
                         'StartTime',
                         'CurrentTime',
                         'StepName',
                         'Session',  # 1 or 2 in Task step, 1 to 3 in VAS step (Beginning-middle-end)
                         'Subtrial',  # From 1 to 49 or 36
                         'ScenarioIndex',
                         'RewardAmount',  # The amount offered for win
                         'PunishmentAmount',  # The amount offered for loss
                         'DistanceAtStart',  # Initial distance from the screen
                         'DistanceAtLock',  # Distance from the screen upon spacebar / 10 seconds
                         'CurrentDistance',
                         'Distance_max',  # Maximal Distance from the Door
                         'Distance_min',  # Minimal Distance from the Door
                         'Distance_lock',
                         'RoundStartTime',
                         'LockTime',  # When did the door lock, Ms
                         'DidDoorOpen',  # 0 or 1
                         'DoorStatus',
                         'DoorOutcome',
                         'DidWin',  # 0 or 1, only if DidDoorOpen is 1!!!
                         'DoorWaitTime',  # How long was the hold before opening the door, Ms
                         'TotalCoins',
                         'VASQuestionNumber',
                         'VASAnswer',
                         'VAS_RT']

    if params['recordPhysio']:
        params['headers'].append('ECG')
        params['headers'].append('EMG')
        params['headers'].append('EDA')

    Df = pandas.DataFrame(columns=params['headers'])
    miniDf = pandas.DataFrame(columns=params['headers'])
    return params, Df, miniDf


def create_dict_for_df(params: dict, **kwargs):
    dictLayout = {}
    for header in params['headers']:
        dictLayout[header] = None

    dictLayout['ExperimentName'] = 'Doors'
    dictLayout['SubjectID'] = params['subjectID']
    dictLayout['StartTime'] = params['startTime']
    for key, value in kwargs.items():
        if key in dictLayout.keys():
            dictLayout[key] = value
    return dictLayout


def export_raw_data(params: dict, Df: pandas.DataFrame):
    Df.to_csv(f'./data/Subject {params["subjectID"]} - fullDF - {datetime.datetime.now().strftime("%Y-%m-%d %H-%M.csv")}')


def export_summarized_dataframe(params: dict, Df:pandas.DataFrame):
    Df.to_csv(f'./data/Subject {params["subjectID"]} - miniDF - {datetime.datetime.now().strftime("%Y-%m-%d %H-%M.csv")}')