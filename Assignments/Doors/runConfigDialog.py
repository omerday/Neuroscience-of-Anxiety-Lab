from psychopy import gui


###############################
# userInputPlay is in charge of gathering initial info for Configuration.
# It includes the subject number and session, the joystick configuration etc.
# Used in the Params section in the main file.
###############################

def user_input_play():
    userInput = gui.Dlg(title="DOORS Task Information")
    userInput.addField('Subject Number:', )
    # userInput.addField('Session:', 1)
    # userInput.addField('Version:', choices=[1, 2])
    userInput.addField('# of Practice Trials:', 5)
    userInput.addField('# of TaskRun1:', choices=[49, 36])
    userInput.addField('# of TaskRun2:', choices=[49, 36])
    userInput.addField('Starting Distance', choices=[50, 'Random'])
    # userInput.addField('# of TaskRun3:', 49)
    # userInput.addField('Trigger Support:', True)
    # userInput.addField('Eyetracker Support:', False)
    userInput.addField('Full Screen', True)
    userInput.addField('Keyboard Mode', False)
    userInput.addField('Joystick Sensitivity (0: very sensitive, 1: normal, 2: less sensitive', 2, choices=[0, 1, 2])
    # userInput.addField('Eyetracker Circle', True)
    # userInput.addField('Sound Mode:',choices=['PTB','Others'])
    return userInput.show()
