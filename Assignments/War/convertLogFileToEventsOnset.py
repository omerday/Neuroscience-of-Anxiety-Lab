import pandas
import sys

subject_id = sys.argv[1]
run = sys.argv[2]
path = sys.argv[3]
try:
    df = pandas.read_csv(path, index_col=False)
except FileExistsError:
    print("File not found!")
    quit()
except:
    print("Failed for unknown error!")
    quit()
df.reset_index(inplace=True, drop=True)

negative_df = df.copy()
negative_df = negative_df[negative_df["Biopac"].isin([31, 32, 33, 34])]
negative_df["duration"] = 3.0
negative_df = negative_df[["Time", "duration"]].round(2)
negative_df.to_csv(f"subject-{subject_id}_run-{run}_negative_events-onset.txt", "\t", index=False)

neutral_df = df.copy()
neutral_df = neutral_df[neutral_df["Biopac"].isin([51, 52, 53, 54])]
neutral_df["duration"] = 3.0
neutral_df = neutral_df[["Time", "duration"]].round(2)
neutral_df.to_csv(f"subject-{subject_id}_run-{run}_neutral_events-onset.txt", "\t", index=False)

positive_df = df.copy()
positive_df = positive_df[positive_df["Biopac"].isin([71, 72, 73, 74])]
positive_df["duration"] = 3.0
positive_df = positive_df[["Time", "duration"]].round(2)
positive_df.to_csv(f"subject-{subject_id}_run-{run}_positive_events-onset.txt", "\t", index=False)

rest_df = df.copy()
rest_df = rest_df[rest_df["Biopac"].isin([22, 24])]
rest_df["duration"] = 3.0
rest_df = rest_df[["Time", "duration"]].round(2)
rest_df.to_csv(f"subject-{subject_id}_run-{run}_rest_events-onset.txt", "\t", index=False)