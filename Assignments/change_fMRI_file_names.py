import os
import sys

FOLDERS_OF_INTEREST={"func":"_task-rest_bold", "anat":"_T1w"}
SUFFIXES=[".json", ".nii.gz"]

path = sys.argv[1]
for folder in os.listdir(path):
    if os.path.isdir(f"{path}/{folder}"):
        for key, value in FOLDERS_OF_INTEREST.items():
            if os.path.exists(f"{path}/{folder}/{key}"):
                for file in os.listdir(f"{path}/{folder}/{key}"):
                    for suffix in SUFFIXES:
                        if file.endswith(suffix):
                            try:
                                print(f"Trying to rename {path}/{folder}/{key}/{file}")
                                os.rename(f"{path}/{folder}/{key}/{file}", f"{path}/{folder}/{key}/{folder}{value}{suffix}")
                            except FileExistsError:
                                print("Failed because the file already exists!")
                            except:
                                print("Failed for unknown error!")
                            else:
                                print("Success!")