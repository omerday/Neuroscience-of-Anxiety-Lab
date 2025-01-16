from psychopy import visual, core

#TODO: change the number of slides
NUM_OF_SLIDES = 30
def instructions(window: visual.Window, params, io):
    keyboard = io.devices.keyboard
    if params['preCond']:
        round = "preCond"
    else:
        round = "test"
    if params['language'] == 'English':
        name_prefix = "Instructions_E_"
    elif params['gender'] == 'Female':
        name_prefix = "Instructions_F_"
    else:
        name_prefix = "Instructions_M_"

    for i in range(1, NUM_OF_SLIDES + 1):
        image = visual.ImageStim(window, image=f"./img/instructions/{round}/{name_prefix}{i}.jpeg", units="norm", size=(2, 2))
        image.draw()
        window.flip()

        # Clearing events list
        keyboard.getKeys()
        core.wait(0.05)

        space = False
        while not space:
            for event in keyboard.getKeys():
                if event.key == "escape":
                    window.close()
                    core.quit()
                elif event.key == " ":
                    space = True
                elif i == 28 and event.key == 'r':
                    instructions(window, params, io)
                    space = True