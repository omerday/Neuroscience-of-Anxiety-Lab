from psychopy import gui


def user_input_play():
    """
    In charge of gathering initial info for configuration using gui.Dlg. it's being inserted into Params dictionary in
    the main file.
    :return: answer array
    """
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
    userInput.addField('Full Screen', True)
    userInput.addField('Keyboard Mode', True)
    userInput.addField('Sensitivity (1: Less sensitive, 2: Normal, 3: More sensitive', 1, choices=[1, 2, 3])
    userInput.addField('Record Physiology', False)
    # userInput.addField('Eyetracker Circle', True)
    # userInput.addField('Sound Mode:',choices=['PTB','Others'])
    return userInput.show()
