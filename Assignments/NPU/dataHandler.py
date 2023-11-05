import pandas as pd
import datetime

HEADERS = [
    'ExpermientName',  # NPU
    'Subject',  # Subject ID
    'StartTime',
    'CurrentTime',
    'ShockType',
    'Block',  # 1 or 2
    'Scenario',  # N, P or U
    'Cue',  # Is cue presented (1 or 0)
    'Startle',  # Startle played (1 or 0, mainly for the miniDF)
    'Shock',  # Shock presented (1 or 0)
    'FearRating'  # (0-10 
    'CueStart',  # a 1-0 representation of when the cue started, for the miniDF
    'CueEnd',  # # a 1-0 representation of when the cue ended, for the miniDF
    'ScenarioIndex'
]


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
    for key, value in kwargs.items():
        if key in dict_layout.keys():
            dict_layout[key] = value
    return dict_layout


def export_raw_data(params: dict, df: pd.DataFrame):
    df.to_csv(
        f'./data/NPU {params["Subject"]} - fullDF - {datetime.datetime.now().strftime("%Y-%m-%d %H-%M.csv")}')


def export_summarized_dataframe(params: dict, mini_df: pd.DataFrame):
    mini_df.to_csv(
        f'./data/NPU {params["Subject"]} - miniDF - {datetime.datetime.now().strftime("%Y-%m-%d %H-%M.csv")}')

