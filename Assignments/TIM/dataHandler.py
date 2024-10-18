import os
import time
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

HEADERS_FMRI_ONSET_FILE = [
    'onset',
    'duration',
    'condition'
]


def setup_data_frame():
    df_pain = pd.DataFrame(columns=HEADERS_PAIN)
    df_mood = pd.DataFrame(columns=HEADERS_MOOD)
    return df_pain, df_mood

def setup_fmri_onset_file():
    return pd.DataFrame(columns=HEADERS_FMRI_ONSET_FILE)


def insert_data_pain(block, trial, temp_number, color, pain, pain_df: pd.DataFrame):
    dict_layout = {}

    for header in HEADERS_PAIN:
        dict_layout[header] = None

    dict_layout['Block'] = block
    dict_layout['Trial'] = trial
    dict_layout['TempNumber'] = temp_number
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

def insert_data_fmri_events(params:dict, duration: float, event: int, event_onset: pd.DataFrame):
    dict = {
        'onset': round(time.time() - params["fmriStartTime"], 2),
        'duration': duration,
        'condition': event,
        }

    return pd.concat([event_onset, pd.DataFrame.from_records(dict)])

def save_fmri_event_onset(params:dict, event_onset_df: pd.DataFrame, block):
    if event_onset_df == None:
        return
    folder = './data'
    if params['subject'] != "":
        folder = f'./data/{params["subject"]}'
        if not os.path.exists(folder):
            os.mkdir(folder)
    event_onset_df.to_csv(f'{folder}/TIM_event_onset_subject_{params["subject"]}_block_{block}.tsv', sep="\t")

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

