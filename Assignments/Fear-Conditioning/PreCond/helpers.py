from psychopy import visual, core

def graceful_shutdown(window):
    print(f"Experiment Ended\n===========================================")
    window.close()
    core.quit()
    exit()
