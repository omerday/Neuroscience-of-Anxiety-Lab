from psychopy import core, event, logging, visual
import time
from psychopy.iohub.client.keyboard import Keyboard
from psychopy.visual import ratingscale
import helpers

PAIN_RATING_QUESTION_HEBREW = ["עד כמה כאב החום?"]
PAIN_RATING_QUESTION_ENGLISH = ["How painful was the heat?"]

PAIN_RATING_ANSWERS_HEBREW = [["0", "01"]]
PAIN_RATING_ANSWERS_ENGLISH = [["0", "10"]]

LABELS = ["Anxiety", "Tiredness", "Worry", "Mood", "PainSensitivity"]

QUESTIONS_HEBREW = ["עד כמה אתם מרגישים חרדה או לחץ כרגע?",
                    "עד כמה אתם עייפים?",
                    "עד כמה אתם מודאגים מהחלק הבא?",
                    "איך מצב הרוח שלכם כרגע?",
                    "עד כמה אתם רגישים לכאב?"]
QUESTIONS_ENGLISH = ["How stressed or anxious are you feeling?",
                     "How tired are you?",
                     "How worried are you for the next part?",
                     "How's your mood right now?",
                     "How sensitive are you to pain?"]

ANSWERS_HEBREW = [["כלל לא", "הרבה מאוד"], ["כלל לא", "הרבה מאוד"], ["כלל לא", "הרבה מאוד"], ["רע מאוד", "טוב מאוד"], ["כלל לא", "הרבה מאוד"]]
ANSWERS_ENGLISH = [["Not at all", "A lot"], ["Not at all", "A lot"], ["Not at all", "A lot"], ["Very good", "Very bad"], ["Not at all", "A lot"]]


def run_vas(window: visual.Window, io, params: dict, type:str, mood_df, pain_df, device, duration=float('inf'), event_onset_df=None):
    if type == "PainRating":
        questions = PAIN_RATING_QUESTION_HEBREW if params['language'] == 'Hebrew' else PAIN_RATING_QUESTION_ENGLISH
        answers = PAIN_RATING_ANSWERS_HEBREW if params['language'] == 'Hebrew' else PAIN_RATING_ANSWERS_ENGLISH
    else:
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
                    helpers.graceful_shutdown(window, params, device, mood_df, pain_df, event_onset_df)
                core.wait(0.05)

        score = scale.getRating()
        if type == "PainRating":
            return score
        else:
            scores[LABELS[i]] = score

    helpers.save_backup(params, Mood=mood_df, Pain=pain_df)
    return scores
