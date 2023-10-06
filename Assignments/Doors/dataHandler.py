import pandas
import time
import datetime
# import bioread
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

HEADERS = ['Time',
           'ExpermientName',
           'SubjectID',
           'StartTime',
           'CurrentTime',
           'Section',
           'Session',
           'Round',  # 1 or 2 in Task step, 1 to 3 in VAS step (Beginning-middle-end)
           'Subtrial',  # From 1 to 49 or 36
           'ScenarioIndex',
           'Reward_magnitude',  # The amount offered for win
           'Punishment_magnitude',  # The amount offered for loss
           'DistanceAtStart',  # Initial distance from the screen
           'DistanceFromDoor_SubTrial',  # Distance from the screen upon spacebar / 10 seconds
           'CurrentDistance',
           'Distance_max',  # Maximal Distance from the Door
           'Distance_min',  # Minimal Distance from the Door
           'Distance_lock',
           'RoundStartTime',
           'DoorAction_RT',  # When did the door lock, Ms
           'Door_opened',  # 0 or 1
           'DoorStatus',
           'Door_outcome',
           'DidWin',  # 0 or 1, only if DidDoorOpen is 1!!!
           'Door_anticipation_time',  # How long was the hold before opening the door, Ms
           'ITI_duration',
           'TotalCoins',
           'VASQuestionNumber',
           'VAS_Answer',
           'VAS_type',
           'VAS_RT',
           'Q_type',
           'Q_score',
           'Q_RT']


def setup_data_frame(params: dict):
    params['headers'] = HEADERS

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
    dictLayout['Session'] = params['Session']
    for key, value in kwargs.items():
        if key in dictLayout.keys():
            dictLayout[key] = value
    return dictLayout


def export_raw_data(params: dict, Df: pandas.DataFrame):
    Df.to_csv(
        f'./data/Doors {params["subjectID"]} - fullDF - {datetime.datetime.now().strftime("%Y-%m-%d %H-%M.csv")}')


def export_summarized_dataframe(params: dict, Df: pandas.DataFrame):
    Df.to_csv(
        f'./data/Doors {params["subjectID"]} - miniDF - {datetime.datetime.now().strftime("%Y-%m-%d %H-%M.csv")}')


def single_subject_analysis(params: dict, ):
    miniDf = pd.read_csv("data/Subject 92313 - miniDF - 2023-10-02 08-24.csv")
    # subject = params["subjectID"]
    dist_df = miniDf[miniDf["Section"].str.contains("TaskRun")]

    # Correlation between R/P amount and the lock distance
    sns.scatterplot(data=dist_df, x="Reward_magnitude", y="DistanceFromDoor_SubTrial", hue="Punishment_magnitude")
    plt.show()

    # Correlation between R/P amount and the lock time
    sns.scatterplot(data=dist_df, x="Reward_magnitude", y="DoorAction_RT", hue="Punishment_magnitude")
    plt.show()

    sns.lineplot(data=dist_df, x="Punishment_magnitude", y="DistanceFromDoor_SubTrial", hue="Reward_magnitude",
                 err_style="band", errorbar="sd")
    plt.show()

