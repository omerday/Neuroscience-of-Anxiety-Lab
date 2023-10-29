import pandas as pd
import sys
import numpy as np

"""
    The script recieves two file paths - the ERA file (result of the SCR matlab script) and the miniDF file from the doors task.
    The script merges info from the miniDF into the era table, according to the scenario index.
    The columns merged:
    
        "Reward_magnitude", 
        "Punishment_magnitude", 
        "DistanceFromDoor_SubTrial", 
        "Door_opened", 
        "Door_outcome"
"""

n = len(sys.argv)
era_path = ""
minidf_path = ""
subjectID = 0

if n < 3:
    print("Not enough arguments entered!\nPlease add the paths to the era file and the miniDF")
    exit()
else:
    era_path = sys.argv[1]
    minidf_path = sys.argv[2]
    subjectID = era_path.split("_")[0].split("/")[-1]

try:
    print(f"Trying to load the era file from {era_path}...")
    era_df = pd.read_csv(era_path, sep="\t")
except:
    print("Loading failed. Please make sure the file exists in the location entered, and that it's tab-seperated.")
    exit()
finally:
    print("Success!")

try:
    print(f"Trying to load the miniDF file from {minidf_path}...")
    mini_df = pd.read_csv(minidf_path)
except:
    print("Loading failed. Please make sure the file exists in the location entered, and that it's comma-seperated.")
    exit()
finally:
    print("Success!")

# Add columns from mini_DF
era_df["Reward_magnitude"] = ""
era_df["Punishment_magnitude"] = ""
era_df["DistanceFromDoor_SubTrial"] = ""
era_df["Door_opened"] = ""
era_df["Door_outcome"] = ""

columns = ["Reward_magnitude", "Punishment_magnitude", "DistanceFromDoor_SubTrial", "Door_opened", "Door_outcome"]

events_list = np.zeros(151)
for index, row in era_df.iterrows():
    scenario = row["Event.NID"]
    numberOfTimes = events_list[scenario]
    for column in columns:
        # print(mini_df[mini_df["ScenarioIndex"] == scenario].iloc[[numberOfTimes]][column])
        era_df.at[index, column] = mini_df[mini_df["ScenarioIndex"] == scenario].iloc[[numberOfTimes]][column].values[0]

    events_list[row["Event.NID"]] += 1

print(era_df.head())

print("All done merging the files!")
era_df.to_csv(f"{subjectID}_era_merged.csv")
print(f"Final result can be found under {subjectID}_era_merged.csv")