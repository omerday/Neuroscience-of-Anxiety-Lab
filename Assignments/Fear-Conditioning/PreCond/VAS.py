from psychopy import core, event, logging, visual
import time
from psychopy.iohub.client.keyboard import Keyboard
from psychopy.visual import ratingscale
import helpers
import dataHadler




LABELS = ["Anxiety", "Tiredness", "Worry", "Mood"]

QUESTIONS_HEBREW = ["עד כמה אתם מרגישים חרדה או לחץ כרגע?",
                    "עד כמה אתם עייפים?",
                    "עד כמה אתם מודאגים מהחלק הבא?",
                    "איך מצב הרוח שלכם כרגע?"]
QUESTIONS_ENGLISH = ["How stressed or anxious are you feeling?",
                     "How tired are you?",
                     "How worried are you for the next part?",
                     "How's your mood right now?"]

ANSWERS_HEBREW = [["כלל לא", "הרבה מאוד"], ["כלל לא", "הרבה מאוד"], ["כלל לא", "הרבה מאוד"], ["רע מאוד", "טוב מאוד"]]
ANSWERS_ENGLISH = [["Not at all", "A lot"], ["Not at all", "A lot"], ["Not at all", "A lot"], ["Very good", "Very bad"]]


def run_vas(window: visual.Window, io, params: dict, type:str, mood_df, duration=float('inf')):
    questions = QUESTIONS_HEBREW if params['language'] == 'Hebrew' else QUESTIONS_ENGLISH
    answers = ANSWERS_HEBREW if params['language'] == 'Hebrew' else ANSWERS_ENGLISH

    keyboard = io.devices.keyboard

    scores = {}

    for i in range(len(questions)):
        scale = ratingscale.RatingScale(window,
                                        labels=[answers[i][0][::-1], answers[i][1][::-1]]
                                            if params['language'] == 'Hebrew' else [answers[i][0],answers[i][1]],
                                        scale=None, choices=None, low=0, high=10, precision=.5, tickHeight=0.5 if type=="PainRating" else 0, size=2,
                                        markerStart=5, noMouse=True, leftKeys='left', rightKeys='right',  # Dummy left and right
                                        textSize=0.6, acceptText="לחצו על הרווח"[::-1] if params['language'] == "Hebrew" else "Press Spacebar", showValue=False, showAccept=True,
                                        acceptPreText="לחצו על הרווח"[::-1] if params['language'] == "Hebrew" else "Press Spacebar", acceptSize=1.5,
                                        markerColor="Maroon", acceptKeys=["space"], textColor="Black",
                                        lineColor="Black", disappear=False)
        question_label = visual.TextStim(window, text=questions[i][::-1] if params['language'] == 'Hebrew' else questions[i], height=.12, units='norm', pos=[0, 0.3], wrapWidth=2,
                                   font="Open Sans", color="Black")

        keyboard.getKeys()
        core.wait(0.05)

        end_time = time.time() + duration
        while (duration != float("inf") and time.time() < end_time) or (duration == float("inf") and scale.noResponse):
            scale.draw()
            question_label.draw()
            window.mouseVisible = False
            window.flip()

            for ev in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
                if ev.key == "escape":
                    helpers.graceful_shutdown(window)
                core.wait(0.05)

        score = scale.getRating()
        scores[LABELS[i]] = score


    dataHadler.save_backup(params, Mood=mood_df)
    return scores
