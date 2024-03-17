# Neuroscience of Anxiety Lab

## Introduction
This repository contains two assignment for anxiety analysis -
- **Doors** - an assignment designated to test the correlation between anxiety and avoidance by giving the subjects different scenarios in which they need to decide whether to approach the trigger or avoid it and lower the chances of negative impact
- **NPU** - an assignment meant to measure the amount of pressure given different situations of uncertainty towards an upcoming threat

We'll supply a brief explanation on each of the tasks, and how to run the code as smoothly as possible.


### 🚪 Doors
The doors task is meant to measure the approach and avoidance of the subject in a given environment.

In each round of the assignment, the subject will encounter 49 doors with an even chance to either win a certain amount of money, or lose a certain (different) amount of money.
They need to decide whether to approach or avoid the door (by going back and forth), increasing or decreasing the chances of the door opening upon the distance from the door.

### ⚡️ NPU
The NPU task's purpose is to measure the physiological reaction to a predictable and unpredictable threats.

In the experiment are three conditions:
Neutral (No threat)
Predictable Threat
Unpredictable Threat

The experiment loops through sequence of condition, and in each of them, for two minutes a cue is shown and disappears from the screen, indicating a possible shock/unpleasent sound.

In the Neutral condition, no shock/unpleasent sound will be given at any time.

In the Predicable Threat condition, a shock/unpleasent sound might be given only when a cue is on the screen.

In the Unpredictable Threat condition, a shock/unpleasent sound might be given at any time, regardless of whether the cue is shown or not.

Randomly, a sound similar to a can opening will be heard, meant to startle the subject and keep them alert (This can be changed in the arguments at the beginning of the task)

## Usage
### Installation
The assignments are available on both Windows and MacOS, but the biopac integration is only supported for Windows devices.

Python 3.8 is required for the code to run.

Before running the assignments, make sure all the required packages are installed using the requirements.txt file provided:
```shell
python -m pip install -r requirements.txt
```
Also, make sure you have Psychopy 2023 installed. Use [this link](https://www.psychopy.org/download.html) for assistance.
### Running the Assignment
Just run the main.py file from the ./Doors or ./NPU folder
### Output
The output for each task includes a few dataframes, saved to ./{task_name}/data folder:
* Full DF - containing continuous data, for each .05 second of the run, in order to be integrated with each sample from the BioPac
* Summary (or mini) DF - containing bottom lines - each unique event that has occured, such as cue onset, startle, door summary etc.