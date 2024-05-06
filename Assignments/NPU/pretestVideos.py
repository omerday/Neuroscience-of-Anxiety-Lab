from psychopy import visual, core, prefs, sound, event
from psychopy.iohub import launchHubServer
from psychopy.iohub.client.keyboard import Keyboard
import pandas as pd
import time
import random
import serialHandler
import serial
import VideosVAS
import dataHandler
import psychtoolbox as ptb

VAS_STRING_HEB = "כעת תתבקשו לענות על מספר שאלות"
VAS_STRING_ENG = "We will now ask you a few questions"

SECOND_VIDEO_HEB = "כעת נעבור לסרטון הבא\nלחצו על הרווח להמשך"
SECOND_VIDEO_ENG = "We will now move on to the next video.\nPress the spacebar to proceed."

STARE_AT_PLUS_1_HEB = "כעת יוצג בפניכם סימן + למשך כדקה,"
STARE_AT_PLUS_2_HEB = "אנא הסתכלו לכיוונו עד שיעלם"

STARE_AT_PLUS_ENG = "You will now be presented with + sign for a minute,\nPlease look at it until it disappears"


def run_videos(win: visual.Window, params: dict, io, ser=None):
    # prefs.hardware['audioLib'] = ['PTB']
    keyboard = io.devices.keyboard
    win.mouseVisible = False
    df = dataHandler.setup_videos_dataframe(params)
    dict_for_df = dataHandler.create_dict_for_videos_df(params)
    rest_time = params['videoRestTime']

    # Show instruction screen
    instructions(win, params, keyboard)

    # Prepare subject for fixation
    fixation_message(win, params, keyboard, 1)

    # Initiate Fixation
    img = visual.ImageStim(win=win, image="./img/plus.jpeg", units='norm', size=(2, 2))
    img.draw()
    win.flip()

    df = report_event_and_add_to_df(params, df, dict_for_df, 50, ser)

    rest_end_time = time.time() + rest_time
    keyboard.getKeys()
    while time.time() < rest_end_time:
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == 'escape':
                quit_gracefully(win, params, df)
        core.wait(0.05)

    del img
    win.flip()

    videos = [r"C:/Users/User/Videos/scarlett-johansson-and-adam-driver-in-marriage-story-l-netflix-no-sound2.mp4",
              r"C:/Users/User/Videos/boringmovie.mp4"]
    audios = [r"C:/Users/User/Videos/Scarlett Johansson and Adam Driver in Marriage Story.wav",
              r"C:/Users/User/Videos/boringmovie.wav"]
    movie_category = ["Exciting", "Boring"]

    random.seed()
    index = 1 if random.uniform(0, 1) > 0.5 else 0

    # Specify the paths to the video and audio files
    video_path = videos[index]
    audio_path = audios[index]
    category = movie_category[index]

    # Show message before first video
    pre_video(win, params, keyboard, 1)

    # Create movie and sound objects
    movie_stim = visual.MovieStim3(win, video_path, flipVert=False, flipHoriz=False, name="movie", autoLog=False)
    audio_stim = sound.Sound(audio_path)

    df = report_event_and_add_to_df(params, df, dict_for_df, 55, ser)

    # Start the audio and video playback
    now = ptb.GetSecs()
    audio_stim.play(when=now)
    movie_stim.setAutoDraw(True)

    keyboard.getKeys()
    # Main loop to keep both audio and video playing until the video finishes
    stop = False
    while movie_stim.status != visual.FINISHED and not stop:
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == 'right':
                audio_stim.stop()
                movie_stim.stop()
                stop = True
            elif event.key == 'escape':
                quit_gracefully(win, params, df)
        movie_stim.draw()
        win.flip()

    # Stop the audio playback when the video finishes
    audio_stim.stop()

    df = report_event_and_add_to_df(params, df, dict_for_df, 60, ser)

    # Show pre-vas message and initiate vas
    vas_message(win, params, keyboard)
    df = VideosVAS.run_vas(win, df, dict_for_df, category, params['language'])

    # Show Fixation message and initiate fixation
    fixation_message(win, params, keyboard, 2)

    img = visual.ImageStim(win=win, image="./img/plus.jpeg", units='norm', size=(2, 2))
    img.draw()
    win.flip()

    df = report_event_and_add_to_df(params, df, dict_for_df, 65, ser)

    rest_end_time = time.time() + rest_time
    keyboard.getKeys()
    while time.time() < rest_end_time:
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == 'escape':
                quit_gracefully(win, params, df)
        core.wait(0.05)

    del img
    win.flip()

    # Show a text message to prompt the user to click
    pre_video(win, params, keyboard, 2)

    # Create a new MovieStim3 object for the second video
    video_path2 = videos[1 - index]
    audio_path2 = audios[1 - index]
    category = movie_category[1 - index]

    # Create movie and sound objects
    movie_stim2 = visual.MovieStim3(win, video_path2, flipVert=False, flipHoriz=False, name="movie2", autoLog=False)
    audio_stim2 = sound.Sound(audio_path2)

    df = report_event_and_add_to_df(params, df, dict_for_df, 70, ser)

    # Start the audio and video playback for the second video
    now = ptb.GetSecs()
    audio_stim2.play(when=now)
    movie_stim2.setAutoDraw(True)

    keyboard.getKeys()
    # Main loop to keep video playing until the second video finishes
    stop = False
    while movie_stim2.status != visual.FINISHED and not stop:
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == 'right':
                audio_stim2.stop()
                movie_stim2.stop()
                stop = True
            elif event.key == 'escape':
                quit_gracefully(win, params, df)
        movie_stim2.draw()
        win.flip()

    # Stop the audio playback when the second video finishes
    audio_stim2.stop()

    df = report_event_and_add_to_df(params, df, dict_for_df, 75, ser)

    vas_message(win, params, keyboard)
    df = VideosVAS.run_vas(win, df, dict_for_df, category, params['language'])

    fixation_message(win, params, keyboard, 2)

    img = visual.ImageStim(win=win, image="./img/plus.jpeg", units='norm', size=(2, 2))
    img.draw()
    win.flip()

    df = report_event_and_add_to_df(params, df, dict_for_df, 79, ser)

    rest_end_time = time.time() + rest_time
    keyboard.getKeys()
    stop = False
    while time.time() < rest_end_time and not stop:
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == 'right':
                audio_stim2.stop()
                movie_stim2.stop()
                stop = True
            if event.key == 'escape':
                quit_gracefully(win, params, df)
        core.wait(0.05)

    del img
    win.flip()

    if params['videosTiming'] == 'Before':
        next_task = visual.ImageStim(win,
                                     f"./img/instructions/videosInstructions/nextTask{params['gender'][0]}{params['language'][0]}.jpeg",
                                     units="norm", pos=(0, 0), size=(2,2))
        next_task.draw()
        win.flip()
        wait_for_space(win, keyboard)

    dataHandler.export_data(params, VideosData=df)


def report_event_and_add_to_df(params: dict, df: pd.DataFrame, dict_for_df: dict, scenario: int, ser=None):
    if params['recordPhysio']:
        serialHandler.report_event(ser, scenario)
        dict_for_df['ScenarioIndex'] = scenario
        dict_for_df['CurrentTime'] = round(time.time() - dict_for_df['StartTime'], 2)
        df = pd.concat([df, pd.DataFrame.from_records([dict_for_df])])
        dict_for_df.pop('ScenarioIndex')
    return df


def instructions(win: visual.Window, params: dict, keyboard):
    if params['videosTiming'] == 'Before':
        curr_instruction = visual.ImageStim(win,
                                            f"./img/instructions/1{params['gender'][0]}{params['language'][0]}.jpeg",
                                            units="norm", pos=(0, 0), size=(2,2))
    else:
        curr_instruction = visual.ImageStim(win,
                                            f"./img/instructions/nextTask{params['gender'][0]}{params['language'][0]}.jpeg",
                                            units="norm", pos=(0, 0), size=(2,2))
    curr_instruction.draw()
    win.flip()
    wait_for_space(win, keyboard)

    curr_instruction = visual.ImageStim(win,
                                        f"./img/instructions/videosInstructions/instruction{params['gender'][0]}{params['language'][0]}.jpeg",
                                        units="norm", pos=(0, 0), size=(2,2))
    curr_instruction.draw()
    win.flip()
    wait_for_space(win, keyboard)


def pre_video(win: visual.Window, params: dict, keyboard, video_num):
    curr_instruction = visual.ImageStim(win,
                                        f"./img/instructions/videosInstructions/video{video_num}{params['gender'][0]}{params['language'][0]}.jpeg",
                                        units="norm", pos=(0, 0), size=(2,2))
    curr_instruction.draw()
    win.flip()
    wait_for_space(win, keyboard)


def fixation_message(win: visual.Window, params: dict, keyboard, instruction: int):
    plus_prep_message = visual.ImageStim(win,
                                         image=f"./img/instructions/videosInstructions/plusPrep{params['gender'][0]}{params['language'][0]}_{instruction}.jpeg",
                                         units="norm", pos=(0, 0), size=(2,2))
    plus_prep_message.draw()
    win.flip()
    wait_for_space(win, keyboard)


def vas_message(win: visual.Window, params: dict, keyboard):
    message = visual.ImageStim(win,
                               f"./img/instructions/videosInstructions/vas{params['gender'][0]}{params['language'][0]}.jpeg",
                               units="norm", pos=(0, 0), size=(2,2))
    message.draw()
    win.flip()
    keyboard.getKeys()
    wait_for_space(win, keyboard)


def wait_for_space(window: visual.Window, keyboard):
    keyboard.getKeys()
    core.wait(0.05)
    while True:
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == ' ':
                return
            elif event.key == 'escape':
                window.close()
                core.quit()
        core.wait(0.05)


def quit_gracefully(window, params, df:pd.DataFrame):
    dataHandler.export_data(params, VideosData=df)
    window.close()
    core.quit()
