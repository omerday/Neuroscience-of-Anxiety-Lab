# NPU (Neutral, Predictable, Unpredictable) Task

Welcome to the NPU Task project! This documentation is designed to help you understand, run, and modify the code, even if you are new to programming or Python.

## What is this Task?

The NPU task is a standard psychological experiment used to measure anxiety and fear. It involves three different conditions:
*   **Neutral (N):** A safe condition where no unpleasant events occur.
*   **Predictable (P):** A threatening condition where an unpleasant event (shock or scream) can occur, but *only* when a specific visual cue (shape) is on the screen. You are safe when the shape is not there.
*   **Unpredictable (U):** A threatening condition where an unpleasant event can occur at *any* time, regardless of whether the shape is on the screen or not.

## Getting Started

### 1. Installation
You will need Python installed (preferably via a standalone **PsychoPy** installation, which includes all necessary libraries). If you are using a standard Python environment, install the dependencies:
```bash
pip install psychopy pandas pyserial openpyxl psychtoolbox
```

### 2. Running the Code
To start the experiment, open your terminal or command prompt, navigate to the project folder, and run:
```bash
python main.py
```

## Configuration (The Startup Dialog)

When you run the code, a window will pop up asking for settings. Here is what they mean:
*   **Subject Number:** The ID for the participant (e.g., 101). This names the output files.
*   **Session:** If the participant is coming back for a second time, change this.
*   **# of Blocks:** How many rounds of the N-P-U sequence to run (1 or 2).
*   **Gender:** Adjusts the instruction text and images (Male/Female).
*   **Preferred Language:** Hebrew or English.
*   **Conditions Sequence:** The order of blocks (e.g., PNUNUNP or UNPNPNU).
*   **Shock Type:** 'Sound' (plays a scream mp3) or 'Shock' (sends a trigger to a shock machine).
*   **Skip Startles:** If checked, the random white noise bursts will be turned off (good for debugging).
*   **Record Physiology:** If checked, the code tries to talk to a BioPac/BioSemi device via USB/Serial. **Uncheck this if testing on a personal laptop.**
*   **Skip Instructions/Calibration:** Shortcuts to jump straight to the game.
*   **Videos Timing:** When to show the movie clips (Before the task, After, or Never).

## Initialization Flow: What happens when you click "OK"?

1.  **Setup:** The code collects your inputs from the dialog.
2.  **Window Creation:** A gray screen is opened.
3.  **Data Setup:** Empty tables (DataFrames) are created to store the results.
4.  **Pre-test Videos:** (If selected) Video clips are played.
5.  **Instructions:** The participant clicks through slides explaining the rules.
6.  **Habituation:** 9 loud noises (startles) are played to get the participant's initial reflex out of the way.
7.  **Baseline Rating:** The participant rates their current anxiety.
8.  **The Game Loop:** The code enters the main loop (N, P, and U blocks).
9.  **Export:** Data is saved to the `data` folder.

## Detailed Code Breakdown

### 1. `main.py` - The Conductor
This is the "boss" file. It doesn't do the heavy lifting itself; instead, it tells other files what to do.
*   **What it does:** Initializes the window, calls the configuration dialog, starts the instruction sequence, loops through the blocks (N, P, U), and finally saves the data.
*   **Key Variable:** `params` - A dictionary (list of settings) that holds everything about the current run (Subject ID, language, settings). It is passed to almost every function.

### 2. `blocksInfra.py` - The Engine
This file contains the logic for running a single "Block" (e.g., one Neutral block of 120 seconds).
*   **`run_condition(...)`:** The main function here. It:
    1.  Decides when the cues (shapes) will appear.
    2.  Decides when the startle sounds will happen.
    3.  Decides when the shock will happen (if it's a P or U block).
    4.  Starts a timer and keeps the block running for 120 seconds.
*   **`wait_in_condition(...)`:** This is the "waiting room". While the screen is showing the background or the shape, this function checks constantly: "Is it time for a startle?", "Is it time for a shock?", "Did the user move the rating mouse?".

### 3. `helpers.py` - The Toolkit
A collection of useful small tools used by everyone else.
*   **`randomize_cue_times()` / `randomize_shock()`:** Complex math to ensure events happen at random but fair times.
*   **`play_startle()` / `play_shock_sound()`:** Handles the audio playback.
*   **`wait_for_space()`:** Pauses the program until the Spacebar is pressed.

### 4. `dataHandler.py` - The Scribe
Responsible for recording everything that happens.
*   **`setup_data_frame()`:** Creates the empty spreadsheets.
*   **`create_dict_for_df()`:** Prepares a single row of data (e.g., "At time 5.2s, user rating was 3").
*   **`export_data()`:** Saves the spreadsheets to `.csv` files in the `data` folder.

### 5. `serialHandler.py` - The Messenger
Handles communication with external lab hardware (like BioPac or BioSemi) to mark events in physiological recordings.
*   **`report_event(ser, event_num)`:** Sends a specific number code (trigger) to the hardware. For example, sending '80' might mark a "Startle" event on the EEG graph.

### 6. `instructionsScreen.py` - The Presenter
Manages the slide shows.
*   **`show_instructions(...)`:** Loops through images 1-36. It handles special slides like the "Shock Example" slide where a sound is actually played.

### 7. `VAS.py` - The Surveyor
Visual Analog Scale (VAS). It asks questions like "How anxious are you?".
*   **`vas(...)`:** Loops through a list of questions (Anxiety, Avoidance, Tiredness, Mood).
*   **`display_vas(...)`:** Draws the actual sliding scale on the screen and waits for the user to click.

### 8. `configDialog.py` - The Receptionist
*   **`get_user_input()`:** Uses PsychoPy's built-in dialog box to ask the experimenter for the session details.

## Data Output

Two files are created for every participant:

1.  **Full DataFrame (`fullDF`):** This is a HUGE file. It records the status of the experiment roughly 60 times per second. Use this if you need continuous ratings (mouse movement) analysis.
2.  **Mini DataFrame (`mini_df`):** This is a SUMMARY file. It only contains rows for specific events (Start of block, Onset of Cue, Shock happened, etc.). This is usually what you want for analysis.

**Common Columns:**
*   `CurrentTime`: Seconds since the start of the experiment.
*   `Scenario`: Which condition are we in? (N, P, U).
*   `Step`: What part of the experiment? (Game, Instructions, etc.).
*   `FearRating`: The 0-10 value from the mouse position.
*   `Shock`/`Startle`: 1 if this event just happened, 0 otherwise.

## Troubleshooting

*   **"Serial Exception" or "Port not found":** You probably have "Record Physiology" checked but no device is connected. Uncheck it in the startup dialog.
*   **Program freezes:** Press `Esc` to force quit. The data collected so far is usually saved in a backup file.