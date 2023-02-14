import sys
sys.path.insert(1, './src')

from psychopy import core, visual, event
from Helper import waitUserSpace,tableWrite,get_keypress
import datetime

# Instruction Session Module.
def InstructionPlay(Df, win, params):
    Dict = {
        "ExperimentName": params['expName'],
        "Subject": params['subjectID'],
        "Session": params["Session"],
        "Version": params["Version"],
        "Section": "Instructions",
        "SessionStartDateTime": datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S"),
    }

    width = params["screenSize"][1] * 1.294
    height = params["screenSize"][1]

    # Display Instruction
    message = visual.TextStim(win, text="Do you want to see the instruction?\n\n(y: Yes, n: No)",units='norm', wrapWidth=3)
    message.draw();
    win.flip();
    c = ['']
    # Wait for user types "y" or "n".
    while (c[0].upper() != "Y" and c[0].upper() != "N"):
        core.wait(1 / 120)
        c = event.waitKeys()  # read a character
        get_keypress(Df,params)

    # If user types "y", run instruction.
    if c[0].upper() == "Y":
        c = ['R']
        while (c[0].upper() == "R"):
            # core.wait(1 / 120)
            for i in range(1, 17):
                imgFile = "./instruction/Slide" + str(i) + ".JPG"
                img1 = visual.ImageStim(win=win, image=imgFile, units="pix", opacity=1, size=(width, height))
                img1.draw();
                win.flip();
                if i == 16:
                    c = event.waitKeys()
                else:
                    waitUserSpace(Df,params)

    # Log the dict result on pandas dataFrame.
    return tableWrite(Df, params,Dict)
