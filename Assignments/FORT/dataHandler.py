import pandas as pd
import datetime
import os
from time import strftime, localtime

HEADERS = [
    'ExpermientName',  # NPU
    'Subject',  # Subject ID
    'Session',
    'StartTime',
    'CurrentTime',
    'Step',  # Game, Instructions or Calibration
    'Block',  # 1 or 2
    'Scenario',  # N, P or U
    'TimeInCondition',
    'Cue',  # Is cue presented (1 or 0)
    'Startle',  # Startle played (1 or 0, mainly for the miniDF)
    'Shock',  # Shock presented (1 or 0)
    'FearRating',  # (0-10)
    'CueStart',  # a 1-0 representation of when the cue started, for the miniDF
    'CueEnd',  # # a 1-0 representation of when the cue ended, for the miniDF
    'ScenarioIndex',
    'InstructionScreenNum',
    'HabituationNum'
    'ShockType',
    'VAS_score',
    'VAS_type',
    'VAS_RT',
]

HEADERS_VIDEOS = ['ExperimentName',
                  'Subject',
                  'Session',
                  'StartTime',
                  'CurrentTime',
                  'MovieCategory',
                  'VAS_score',
                  'VAS_type',
                  'VAS_RT',
                  'ScenarioIndex']


def setup_data_frame(params: dict):
    params['headers'] = HEADERS

    df = pd.DataFrame(columns=params['headers'])
    mini_df = pd.DataFrame(columns=params['headers'])
    return params, df, mini_df


def create_dict_for_df(params: dict, **kwargs):
    dict_layout = {}
    for header in params['headers']:
        dict_layout[header] = None

    dict_layout['ExperimentName'] = 'NPU'
    dict_layout['Subject'] = params['Subject']
    dict_layout['StartTime'] = params['startTime']
    dict_layout["Session"] = params['session']
    dict_layout["ShockType"] = params["shockType"]
    for key, value in kwargs.items():
        if key in dict_layout.keys():
            dict_layout[key] = value
    return dict_layout


def export_raw_data(params: dict, df: pd.DataFrame):
    df = df.drop_duplicates(keep='first')
    df.to_csv(
        f'./data/NPU {params["Subject"]} - fullDF - {datetime.datetime.now().strftime("%Y-%m-%d %H-%M.csv")}')


def export_summarized_dataframe(params: dict, mini_df: pd.DataFrame):
    mini_df = mini_df.drop_duplicates(keep='first')
    mini_df.to_csv(
        f'./data/NPU {params["Subject"]} - miniDF - {datetime.datetime.now().strftime("%Y-%m-%d %H-%M.csv")}')


def export_data(params: dict, **kwargs):
    folder = './data'
    if params['Subject'] != "":
        folder = f'./data/{params["Subject"]}'
        if not os.path.exists(folder):
            os.mkdir(folder)

    for key, value in kwargs.items():
        if isinstance(value, pd.DataFrame):
            try:
                df = value.drop_duplicates(keep='first')
                df.to_csv(
                    f'{folder}/NPU {params["Subject"]} Session {params["session"]} - {key} - {strftime("%Y-%m-%d %H-%M", localtime(params["startTime"]))}.csv')
            except:
                print("Something went wrong, keeping backup")
            else:
                backup_path = f'{folder}/NPU {params["Subject"]} Session {params["session"]} - {key} - {strftime("%Y-%m-%d %H-%M", localtime(params["startTime"]))}.backup.csv'
                if os.path.exists(backup_path):
                    os.remove(backup_path)


def save_backup(params: dict, **kwargs):
    folder = './data'
    if params['Subject'] != "":
        folder = f'./data/{params["Subject"]}'
        if not os.path.exists(folder):
            os.mkdir(folder)

    for key, value in kwargs.items():
        if isinstance(value, pd.DataFrame):
            df = value.drop_duplicates(keep='first')
            df.to_csv(
                f'{folder}/NPU {params["Subject"]} Session {params["session"]} - {key} - {strftime("%Y-%m-%d %H-%M", localtime(params["startTime"]))}.backup.csv')


def setup_videos_dataframe(params: dict):
    df = pd.DataFrame(columns=HEADERS_VIDEOS)
    return df


def create_dict_for_videos_df(params: dict, **kwargs):
    dict_layout = {}
    for header in HEADERS_VIDEOS:
        dict_layout[header] = None

    dict_layout['ExperimentName'] = 'NPU'
    dict_layout['Subject'] = params['Subject']
    dict_layout['StartTime'] = params['startTime']
    dict_layout["Session"] = params['session']

    for key, value in kwargs.items():
        dict_layout[key] = value
    return dict_layout
