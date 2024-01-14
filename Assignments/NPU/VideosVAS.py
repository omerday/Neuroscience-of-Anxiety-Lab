import pandas as pd
from psychopy import event, core, visual
from psychopy.iohub import launchHubServer
from psychopy.iohub.client.keyboard import Keyboard
from psychopy.visual import ratingscale

QUESTION_LABELS = ["Happiness", "Anger", "Worry", "Discomfort", "Sadness", "Ending"]
QUESTIONS_HEBREW = ["כמה הרגשתם שמחה בזמן צפיית הסרט?",
                      "כמה הרגשתם כועסים בזמן צפיית הסרט ?",
                      "כמה  הרגשתם דאגה/חשש בזמן צפיית הסרט ?",
                      "כמה הרגשתם אי נוחות בזמן צפיית הסרט?",
                      "כמה הרגשתם עצב בזמן צפיית הסרט?",
                      "?כמה רציתם שהסרט יגמר"]

QUESTIONS_ENGLISH = ["How happy did you feel while watching the movie?",
                      "How angry did you feel while watching the movie?",
                      "What anxiety/apprehension did you feel while watching the movie?",
                      "What discomfort did you feel while watching the movie?",
                      "What sadness did you feel while watching the movie?",
                      "How much you want the movie to end?"]

YES_NO_LABEL = ["Watched Before", "Eyes Closed"]
YES_NO_QUESTIONS_HEBREW = ["?האם ראית את הקטע וידאו בעבר",
                              "האם עצמתם את העיניים או הסתכלם הצידה במהלך הצפייה בקטע הוידאו?"]
YES_NO_QUESTIONS_ENGLISH = ["Had you seen this film before?",
                              "Did you close your eyes or look away during any scenes?"]

ANSWERS_HEBREW = ["כלל לא", "במידה רבה"]
ANSWERS_ENGLISH = ["Not at all", "Very much"]

YES_NO_HEBREW = ["לא", "כן"]
YES_NO_ENGLISH = ["No", "Yes"]


def run_vas(window: visual.Window, df:pd.DataFrame, dict_for_df: dict, category: str, language="Hebrew"):

    dict_for_df['MovieCategory'] = category
    i = 0

    for question in QUESTIONS_HEBREW if language == "Hebrew" else QUESTIONS_ENGLISH:
        question_text = visual.TextStim(win=window, text=question[::-1] if language=="Hebrew" else question, height=.12, units='norm', pos=[0, 0.3], wrapWidth=2,
                                   font="Open Sans", color="Black")
        scale = ratingscale.RatingScale(win=window, scale=None, low=0, high=8, precision=1, tickHeight=1, size=2,
                                        markerStart=4, noMouse=True, leftKeys='left', rightKeys='right',
                                        textSize=0.6, acceptText='Continue', showValue=False, showAccept=True,
                                        acceptPreText="לחצו על הרווח"[::-1] if language == "Hebrew" else "Press Spacebar", acceptSize=1.5,
                                        markerColor="Maroon", acceptKeys=["space", " "], textColor="Black", lineColor="Black", disappear=False,
                                        labels=[ANSWERS_HEBREW[0][::-1], ANSWERS_HEBREW[1][::-1]] if language == "Hebrew" else ANSWERS_ENGLISH)
        question_text.draw()
        scale.draw()
        window.flip()

        while scale.noResponse:
            question_text.draw()
            scale.draw()
            window.flip()
            core.wait(0.05)

        print(scale.getRating())
        dict_for_df['VAS_score'] = scale.getRating()
        dict_for_df['VAS_type'] = QUESTION_LABELS[i]
        dict_for_df['VAS_RT'] = scale.getRT()
        df = pd.concat([df, pd.DataFrame.from_records([dict_for_df])])
        i += 1
        del question_text
        del scale

    i = 0
    for question in YES_NO_QUESTIONS_HEBREW if language == "Hebrew" else YES_NO_QUESTIONS_ENGLISH:
        question_text = visual.TextStim(win=window, text=question[::-1] if language=="Hebrew" else question, height=.12, units='norm', pos=[0, 0.3], wrapWidth=2,
                                        font="Open Sans", color="Black")
        scale = ratingscale.RatingScale(win=window, scale=None, low=0, high=1, precision=1, tickHeight=1, size=2,
                                        markerStart=0, noMouse=True, leftKeys='left', rightKeys='right',
                                        textSize=0.6, acceptText='Continue', showValue=False, showAccept=True,
                                        acceptPreText="לחצו על הרווח"[::-1] if language == "Hebrew" else "Press Spacebar",
                                        acceptSize=1.5,
                                        markerColor="Maroon", acceptKeys=["space", " "], textColor="Black",
                                        lineColor="Black", disappear=False,
                                        labels=[YES_NO_HEBREW[0][::-1],
                                                YES_NO_HEBREW[1][::-1]] if language == "Hebrew" else YES_NO_ENGLISH)
        question_text.draw()
        scale.draw()
        window.flip()

        while scale.noResponse:
            question_text.draw()
            scale.draw()
            window.flip()
            core.wait(0.05)

        dict_for_df['VAS_score'] = scale.getRating()
        dict_for_df['VAS_type'] = QUESTION_LABELS[i]
        dict_for_df['VAS_RT'] = scale.getRT()
        df = pd.concat([df, pd.DataFrame.from_records([dict_for_df])])
        i += 1
        del question_text
        del scale

    return df
