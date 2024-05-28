import os
from time import strftime, localtime
import pandas as pd

HEADERS_PAIN = [
    'Block',
    'Trial',
    'TempNumber',
    'Color'
    'Pain',
]

HEADERS_MOOD = [
    'Round',
    'Label',
    'Score'
]


def setup_data_frame():
    df_pain = pd.DataFrame(columns=HEADERS_PAIN)
    df_mood = pd.DataFrame(columns=HEADERS_MOOD)
    return df_pain, df_mood


def insert_data_pain(Block, trial, tempNumber, color, pain, pain_df: pd.DataFrame):
    dict_layout = {}

    for header in HEADERS_PAIN:
        dict_layout[header] = None

    dict_layout['Block'] = Block
    dict_layout['Trial'] = trial
    dict_layout['TempNumber'] = tempNumber
    dict_layout["Color"] = color
    dict_layout["Pain"] = pain

    pain_df = pd.concat([pain_df, pd.DataFrame.from_records([dict_layout])])

    return pain_df


def insert_data_mood(round: str, scores, mood_df: pd.DataFrame):
    dict_layout = {}

    for header in HEADERS_MOOD:
        dict_layout[header] = None

    for key, value in scores.items():
        dict_layout['Round'] = round
        dict_layout['Label'] = key
        dict_layout['Score'] = value
        mood_df = pd.concat([mood_df, pd.DataFrame.from_records([dict_layout])])

    return mood_df

def export_data(params: dict, **kwargs):
    folder = './data'
    if params['subject'] != "":
        folder = f'./data/{params["subject"]}'
        if not os.path.exists(folder):
            os.mkdir(folder)

    for key, value in kwargs.items():
        if isinstance(value, pd.DataFrame):
            try:
                df = value.drop_duplicates(keep='first')
                df.to_csv(
                    f'{folder}/TIM {params["subject"]} Session {params["session"]} - {key} - {strftime("%d-%m-%Y %H-%M", localtime(params["startTime"]))}.csv')
            except:
                print("Something went wrong, keeping backup")
            else:
                backup_path = f'{folder}/TIM {params["subject"]} Session {params["session"]} - {key} - {strftime("%d-%m-%Y %H-%M", localtime(params["startTime"]))}.backup.csv'
                if os.path.exists(backup_path):
                    os.remove(backup_path)


def save_backup(params: dict, **kwargs):
    folder = './data'
    if params['subject'] != "":
        folder = f'./data/{params["subject"]}'
        if not os.path.exists(folder):
            os.mkdir(folder)

    for key, value in kwargs.items():
        if isinstance(value, pd.DataFrame):
            df = value.drop_duplicates(keep='first')
            df.to_csv(
                f'{folder}/TIM {params["subject"]} Session {params["session"]} - {key} - {strftime("%d-%m-%Y %H-%M", localtime(params["startTime"]))}.backup.csv')

