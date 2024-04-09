from psychopy import visual
import random


def square_run(window: visual.Window, params: dict):
    repeats = params['nTrials'] // len(params['color'])
    colors_order = []
    for color in params['colors']:
        for i in range(repeats):
            colors_order.append(color)
    while colors_order:
        curr_color = random.choice(colors_order)
        colors_order.remove(curr_color)
        if curr_color == 'Green':
            temp = params['T2']
        elif curr_color == 'Yellow':
            temp = params['T4']
        elif curr_color == 'Red':
            temp = params['T6']
