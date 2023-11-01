import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

DIST_HEADERS = ["Section", "Session", "Round", "Subtrial", 'ScenarioIndex','Reward_magnitude', 'Punishment_magnitude',
           'DistanceAtStart', 'DistanceFromDoor_SubTrial', 'CurrentDistance', 'Distance_max', 'Distance_min',
           'Distance_lock', 'DoorAction_RT', 'Door_opened', 'DoorStatus', 'Door_outcome',
           'DidWin', 'Door_anticipation_time', 'ITI_duration',]
VAS_HEADERS = ["Section", 'VASQuestionNumber', 'VAS_score', 'VAS_type', 'VAS_RT',]

def analyze_subject(subject_id: int):
    df = None
    for root, dirs, files in os.walk("./data"):
        for file in files:
            if str(subject_id) in file and "miniDF" in file:
                df = pd.read_csv("./data/" + file)
    if df is None:
        return
    dist_df = df[df["Section"].str.contains("TaskRun")]
    dist_df = dist_df[DIST_HEADERS]

    vas_df = df[df["Section"].str.contains("VAS")]
    vas_df = vas_df[VAS_HEADERS]


def analyze_group():
    # This part is in charge of extracting other subject's data in order to create a collective data analysis
    if os.path.exists("./data/subjects.csv"):
        subjects = pd.read_csv("./data/subjects.csv")
        subject_list = []
        for index, row in subjects.iterrows():
            subject_list.append(row["Subject"])
