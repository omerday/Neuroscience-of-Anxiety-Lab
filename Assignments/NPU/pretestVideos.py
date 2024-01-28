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
VAS_STRING_ENG = "You are now asked to answer a few questions"

SECOND_VIDEO_HEB = "כעת נעבור לסרטון הבא\nלחצו על הרווח להמשך"
SECOND_VIDEO_ENG = "We will now move on to the next video.\nPress the spacebar to proceed."

STARE_AT_PLUS_1_HEB = "כעת יוצג בפניכם סימן של פלוס."
STARE_AT_PLUS_2_HEB = "אנא הסתכלו לכיוונו עד שיעלם"

STARE_AT_PLUS_ENG = "You will now be presented with a plus sign.\nPlease look directly to it until it disappears."


def run_post_videos(win: visual.Window, params: dict, io, ser=None):
    # prefs.hardware['audioLib'] = ['PTB']
    keyboard = io.devices.keyboard
    df = dataHandler.setup_videos_dataframe(params)
    dict_for_df = dataHandler.create_dict_for_videos_df(params)

    rest_time = params['videoRestTime']

    plus_stare_message(win, params, keyboard)

    img = visual.ImageStim(win=win, image="./img/plus.jpeg", units='norm', size=(2, 2))
    img.draw()
    win.flip()

    df = report_event_and_add_to_df(params, df, dict_for_df, 50, ser)

    rest_end_time = time.time() + rest_time
    keyboard.getKeys()
    while time.time() < rest_end_time:
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == 'escape':
                print("escape key pressed, quitting")
                win.close()
                core.quit()
        core.wait(0.05)

    del img
    win.flip()

    textHello = visual.TextStim(win=win,
                                text='עכשיו אתם עומדים לצפות בקטע וידאו' if params["language"] == "Hebrew"
                                else "You are now about to watch a video clip", font='Arial',
                                pos=(0, 0), height=0.12, wrapWidth=1, ori=0.0, units="norm",
                                color='#000000', languageStyle='RTL' if params["language"] == "Hebrew" else "LTR")

    # draw the text
    textHello.draw()

    # Show the window and wait 5 sec
    win.flip()
    press = False
    keyboard.getKeys()
    while not press:
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == ' ':
                press = True
            elif event.key == 'escape':
                win.close()
                core.quit()
        core.wait(0.05)

    videos = [r"C:/Users/User/Videos/scarlett-johansson-and-adam-driver-in-marriage-story-l-netflix-no-sound2.mp4",
              r"C:/Users/User/Videos/boring-short-video_8yidKDJ9.mp4"]
    audios = [r"C:/Users/User/Videos/Scarlett Johansson and Adam Driver in Marriage Story.wav",
              r"C:/Users/User/Videos/boring-short-video_IJ43b94a2.wav"]
    movie_category = ["Exciting", "Boring"]

    index = random.randint(0, 1)

    # Specify the paths to the video and audio files
    video_path = videos[index]
    audio_path = audios[index]
    category = movie_category[index]

    # Create movie and sound objects
    movie_stim = visual.MovieStim3(win, video_path, flipVert=False, flipHoriz=False, name="movie", autoLog=False)
    audio_stim = sound.Sound(audio_path)

    # Show a text message to prompt the user to click
    click_prompt = visual.TextStim(win, text="לחצו על מקש הרווח להפעלת הוידאו" if params["language"] == "Hebrew"
                                else "Click the spacebar to start the video", pos=(0, 0),
                                   height=0.12, wrapWidth=1, ori=0.0,
                                   units="norm", color="#000000",
                                   languageStyle='RTL' if params["language"] == "Hebrew" else "LTR")

    press = False
    keyboard.getKeys()
    while not press:
        click_prompt.draw()
        win.flip()
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == ' ':
                press = True
            elif event.key == 'escape':
                win.close()
                core.quit()
        core.wait(0.05)

    df = report_event_and_add_to_df(params, df, dict_for_df, 10, ser)

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
                win.close()
                core.quit()
        movie_stim.draw()
        win.flip()

    # Stop the audio playback when the video finishes
    audio_stim.stop()

    df = report_event_and_add_to_df(params, df, dict_for_df, 60, ser)

    df = VideosVAS.run_vas(win, df, dict_for_df, category, params['language'])

    plus_stare_message(win, params, keyboard)

    img = visual.ImageStim(win=win, image="./img/plus.jpeg", units='norm', size=(2, 2))
    img.draw()
    win.flip()

    df = report_event_and_add_to_df(params, df, dict_for_df, 65, ser)

    rest_end_time = time.time() + rest_time
    keyboard.getKeys()
    while time.time() < rest_end_time:
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == 'escape':
                win.close()
                core.quit()
        core.wait(0.05)

    del img
    win.flip()

    # Show a text message to prompt the user to click
    click_prompt = visual.TextStim(win, text=SECOND_VIDEO_HEB if params["language"] == "Hebrew"
                                else SECOND_VIDEO_ENG, pos=(0, 0),
                                   height=0.12, wrapWidth=1, ori=0.0,
                                   units="norm", color="#000000",
                                   languageStyle='RTL' if params["language"] == "Hebrew" else "LTR")

    press = False
    keyboard.getKeys()
    while not press:
        click_prompt.draw()
        win.flip()
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == ' ':
                press = True
            elif event.key == 'escape':
                win.close()
                core.quit()
        core.wait(0.05)

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
                win.close()
                core.quit()
        movie_stim2.draw()
        win.flip()

    # Stop the audio playback when the second video finishes
    audio_stim2.stop()

    df = report_event_and_add_to_df(params, df, dict_for_df, 75, ser)
    df = VideosVAS.run_vas(win, df, dict_for_df, category, params['language'])

    plus_stare_message(win, params, keyboard)

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
                print("escape key pressed, quitting")
                win.close()
                core.quit()
        core.wait(0.05)

    del img
    win.flip()

    dataHandler.export_data(params, VideosData=df)


def report_event_and_add_to_df(params: dict, df: pd.DataFrame, dict_for_df: dict, scenario: int, ser=None):
    if params['recordPhysio']:
        serialHandler.report_event(ser, scenario)
        dict_for_df['ScenarioIndex'] = scenario
        dict_for_df['CurrentTime'] = round(time.time() - dict_for_df['StartTime'], 2)
        df = pd.concat([df, pd.DataFrame.from_records([dict_for_df])])
        dict_for_df.pop('ScenarioIndex')
    return df


def plus_stare_message(win:visual.Window, params:dict, keyboard):
    plus_stare = visual.TextStim(win=win, text=STARE_AT_PLUS_1_HEB + "\n" + STARE_AT_PLUS_2_HEB if
                                params['language'] == 'Hebrew' else STARE_AT_PLUS_ENG,
                                 font='Arial', pos=(0, 0), height=0.12, wrapWidth=1, ori=0.0, units="norm",
                                 color='#000000', languageStyle='RTL' if params["language"] == "Hebrew" else "LTR"
                                 )
    plus_stare.draw()
    win.flip()
    press = False
    keyboard.getKeys()
    while not press:
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == ' ':
                press = True
            elif event.key == 'escape':
                win.close()
                core.quit()
        core.wait(0.05)
    del plus_stare


def vas_message(win:visual.Window, params:dict, keyboard):
    vas_text = visual.TextStim(win=win, text=VAS_STRING_HEB if params['language'] == 'Hebrew' else VAS_STRING_ENG,
                                 font='Arial', pos=(0, 0), height=0.12, wrapWidth=1, ori=0.0, units="norm",
                                 color='#000000', languageStyle='RTL' if params["language"] == "Hebrew" else "LTR"
                                 )
    vas_text.draw()
    win.flip()
    press = False
    keyboard.getKeys()
    while not press:
        for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
            if event.key == ' ':
                press = True
            elif event.key == 'escape':
                win.close()
                core.quit()
        core.wait(0.05)
    del vas_text