import os
import pandas as pd
from time import strftime, localtime

HEADERS_MOOD = [
    'Round',
    'Label',
    'Score'
]

def setup_data_frame():
    return pd.DataFrame(columns=HEADERS_MOOD)

def insert_data_mood(round: str, scores: dict, mood_df: pd.DataFrame) -> pd.DataFrame:
    """
    Insert mood data into the mood DataFrame.

    Args:
        round (str): Identifier for the round.
        scores (dict): A dictionary of mood labels and their scores.
        mood_df (pd.DataFrame): Existing mood DataFrame.

    Returns:
        pd.DataFrame: Updated mood DataFrame.
    """
    dict_layout = {header: None for header in HEADERS_MOOD}

    for key, value in scores.items():
        dict_layout['Round'] = round
        dict_layout['Label'] = key
        dict_layout['Score'] = value
        mood_df = pd.concat([mood_df, pd.DataFrame.from_records([dict_layout])])

    return mood_df

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
                f'{folder}/Fear-Conditioning/PreCond/ {params["subject"]} Session {params["session"]} - {key} - {strftime("%d-%m-%Y %H-%M", localtime(params["startTime"]))}.backup.csv')

