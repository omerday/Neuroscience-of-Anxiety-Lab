from psychopy import core, event, logging, visual
import time
from psychopy.iohub.client.keyboard import Keyboard
from psychopy.visual import ratingscale

MOOD_RATING_QUESTION_HEBREW = "עד כמה כאב החום?"
MOOD_RATING_QUESTION_ENGLISH = "How painful was the heat?"

MOOD_RATING_ANSWERS_HEBREW = ["בכלל לא", "מאוד"]
MOOD_RATING_ANSWERS_ENGLISH = ["Not at all", "A lot"]

LABELS = ["Anxiety", "Tiredness", "Worry", "Mood", "PainSensitivity"]

QUESTIONS_HEBREW = ["עד כמה אתם מרגישים חרדה או לחץ כרגע?",
                    "עד כמה אתם עייפים?",
                    "עד כמה אתם מודאגים מהחלק הבא?",
                    "איך מצב הרוח שלכם כרגע?",
                    "עד כמה אתם רגישים לכאב?"]
QUESTIONS_ENGLISH = ["How stressed or anxious are you feeling?",
                     "How tired are you?",
                     "How worried are you from the next part?",
                     "How's your mood right now?",
                     "How sensitive are you to pain?"]

ANSWERS_HEBREW = [["כלל לא", "הרבה מאוד"], ["כלל לא", "הרבה מאוד"], ["כלל לא", "הרבה מאוד"], ["רע מאוד", "טוב מאוד"], ["כלל לא", "הרבה מאוד"]]
ANSWERS_ENGLISH = [["Not at all", "A lot"], ["Not at all", "A lot"], ["Not at all", "A lot"], ["Very good", "Very bad"], ["Not at all", "A lot"]]

def run_vas(window: visual.Window, io, params: dict, type:str, duration=float('inf')):
    if type == "PainRating":
        questions = MOOD_RATING_QUESTION_HEBREW if params['language'] == 'Hebrew' else MOOD_RATING_QUESTION_ENGLISH
        answers = MOOD_RATING_ANSWERS_HEBREW if params['language'] == 'Hebrew' else MOOD_RATING_ANSWERS_ENGLISH
    else:
        questions = QUESTIONS_HEBREW if params['language'] == 'Hebrew' else QUESTIONS_ENGLISH
        answers = ANSWERS_HEBREW if params['language'] == 'Hebrew' else ANSWERS_ENGLISH

    keyboard = io.devices.keyboard

    scores = {}

    for i in range(len(questions)):
        scale = ratingscale.RatingScale(window,
                                        labels=[answers[i][0][::-1], answers[i][1][::-1]]
                                            if params['language'] == 'Hebrew' else [answers[i][0],answers[i][1]],
                                        scale=None, choices=None, low=1, high=100, precision=1, tickHeight=0, size=2,
                                        markerStart=50, noMouse=True, leftKeys=1, rightKeys=2,  # Dummy left and right
                                        textSize=0.6, acceptText="לחצו על הרווח"[::-1] if params['language'] == "Hebrew" else "Press Spacebar", showValue=False, showAccept=True,
                                        acceptPreText="לחצו על הרווח"[::-1] if params['language'] == "Hebrew" else "Press Spacebar", acceptSize=1.5,
                                        markerColor="Maroon", acceptKeys=["space"], textColor="Black",
                                        lineColor="Black", disappear=False)
        question_label = visual.TextStim(window, text=questions[i][::-1] if params['language'] == 'Hebrew' else questions[i], height=.12, units='norm', pos=[0, 0.3], wrapWidth=2,
                                   font="Open Sans", color="Black")

        core.wait(0.05)
        keyboard.getKeys()

        end_time = time.time() + duration
        accept = False
        while (duration != float(inf) and time.time() < end_time) or (duration == float(inf) and scale.noResponse and not accept):
            scale.draw()
            question_label.draw()
            window.flip()
            for event in keyboard.getKeys(etype=Keyboard.KEY_PRESS):
                if event.key in ["left", "right"]:
                    key_hold = True
                    step = 1 if event.key == "right" else -1
                    while key_hold:
                        scale.markerPlacedAt = max(scale.markerPlacedAt + step, scale.low)
                        scale.markerPlacedAt = min(scale.markerPlacedAt + step, scale.high)
                        scale.draw()
                        question_label.draw()
                        window.flip()
                        for releaseEvent in keyboard.getKeys(etype=Keyboard.KEY_RELEASE):
                            key_hold = False
                            if releaseEvent.key in [' ', 'space']:
                                accept = True
                            elif releaseEvent.key == 'escape':
                                window.close()
                                core.quit()
                        core.wait(0.03)
                elif event.key in [" ", "space"]:
                    accept = True
                    break
                elif event.key == "escape":
                    window.close()
                    core.quit()
        score = scale.getRating()
        if type == "PainRating":
            return score
        else:
            scores[LABELS[i]] = score
    return scores