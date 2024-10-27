import random
import os
import cv2
import time
from datetime import datetime
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
from tkinter import Canvas
from enum import Enum
import pandas as pd
import ctypes
import serial
from serialHandler import EVENTS_ENCODING, report_event
import win32gui


SCALE_FACTOR = 0.9
GRID_PATH = "WAR_images/Utils/Grid.jpg"
OPENING_SLIDE1_PATH = "WAR_images/Utils/OpeningSlide1.JPG"
OPENING_SLIDE2_PATH = "WAR_images/Utils/OpeningSlide2.JPG"
OPENING_SLIDE3_PATH = "WAR_images/Utils/OpeningSlide3.JPG"
OPENING_SLIDE4_PATH = "WAR_images/Utils/OpeningSlide4.JPG"
OPENING_SLIDE5_PATH = "WAR_images/Utils/OpeningSlide5.JPG"
OPENING_SLIDES = [OPENING_SLIDE1_PATH, OPENING_SLIDE2_PATH, OPENING_SLIDE3_PATH, OPENING_SLIDE4_PATH,
                  OPENING_SLIDE5_PATH]
USER_INPUT_IMAGE_PATH = "WAR_images/Utils/UserInput.jpg"
START_IMAGE_PATH = "WAR_images/Utils/Start.jpeg"
NEG_IMAGES_BASE_PATH = "WAR_images/NegImages"
NEUT_IMAGES_BASE_PATH = "WAR_images/NeutImages"
POS_IMAGES_BASE_PATH = "WAR_images/PosImages"
PLUS_IMAGE_PATH = "WAR_images/Utils/Plus.jpeg"
EMOTIONAL_SCALE_POS_IMAGE_PATH = "WAR_images/Utils/EmotionalScalePos.jpeg"
EMOTIONAL_SCALE_NEG_IMAGE_PATH = "WAR_images/Utils/EmotionalScaleNeg.jpeg"
EMOTIONAL_SLIDE_PREVIEW_PATH = "WAR_images/Utils/EmotionalSlidesPreview.JPG"
NEG_BLOCK_START_PATH = "WAR_images/Utils/NegBlockStart.jpg"
NEUT_BLOCK_START_PATH = "WAR_images/Utils/NeutBlockStart.jpg"
POS_BLOCK_START_PATH = "WAR_images/Utils/PosBlockStart.jpg"
LONG_REST_PATH = "WAR_images/Utils/LongRest.jpeg"
SHORT_REST_IMAGE_PATH = "WAR_images/Utils/ShortRest.jpeg"
END_SLIDE_PATH = "WAR_images/Utils/EndSlide.jpg"
WASHOUT_START_IMAGE_PATH = "WAR_images/Utils/WashoutStart.jpeg"
WASHOUT_SCALE_IMAGE_PATH = "WAR_images/Utils/WashoutScale.JPG"
WASHOUT_SET1_IMAGE1_PATH = "WAR_images/Utils/Set1Shape1.JPG"
WASHOUT_SET1_IMAGE1D_PATH = "WAR_images/Utils/Set1Shape1D.JPG"
WASHOUT_SET1_IMAGE1_DOTS = 1
WASHOUT_SET1_IMAGE2_PATH = "WAR_images/Utils/Set1Shape2.JPG"
WASHOUT_SET1_IMAGE2D_PATH = "WAR_images/Utils/Set1Shape2D.JPG"
WASHOUT_SET1_IMAGE2_DOTS = 3
WASHOUT_SET1_IMAGE3_PATH = "WAR_images/Utils/Set1Shape3.JPG"
WASHOUT_SET1_IMAGE3D_PATH = "WAR_images/Utils/Set1Shape3D.JPG"
WASHOUT_SET1_IMAGE3_DOTS = 4
WASHOUT_SET1_IMAGE4_PATH = "WAR_images/Utils/Set1Shape4.JPG"
WASHOUT_SET1_IMAGE4D_PATH = "WAR_images/Utils/Set1Shape4D.JPG"
WASHOUT_SET1_IMAGE4_DOTS = 3
WASHOUT_SET2_IMAGE1_PATH = "WAR_images/Utils/Set2Shape1.JPG"
WASHOUT_SET2_IMAGE1D_PATH = "WAR_images/Utils/Set2Shape1D.JPG"
WASHOUT_SET2_IMAGE1_DOTS = 2
WASHOUT_SET2_IMAGE2_PATH = "WAR_images/Utils/Set2Shape2.JPG"
WASHOUT_SET2_IMAGE2D_PATH = "WAR_images/Utils/Set2Shape2D.JPG"
WASHOUT_SET2_IMAGE2_DOTS = 2
WASHOUT_SET2_IMAGE3_PATH = "WAR_images/Utils/Set2Shape3.JPG"
WASHOUT_SET2_IMAGE3D_PATH = "WAR_images/Utils/Set2Shape3D.JPG"
WASHOUT_SET2_IMAGE3_DOTS = 2
WASHOUT_SET2_IMAGE4_PATH = "WAR_images/Utils/Set2Shape4.JPG"
WASHOUT_SET2_IMAGE4D_PATH = "WAR_images/Utils/Set2Shape4D.JPG"
WASHOUT_SET2_IMAGE4_DOTS = 5

WASHOUT_SET1_IMAGES = [WASHOUT_SET1_IMAGE1_PATH, WASHOUT_SET1_IMAGE2_PATH, WASHOUT_SET1_IMAGE3_PATH,
                       WASHOUT_SET1_IMAGE4_PATH]
WASHOUT_SET1D_IMAGES = [WASHOUT_SET1_IMAGE1D_PATH, WASHOUT_SET1_IMAGE2D_PATH, WASHOUT_SET1_IMAGE3D_PATH,
                       WASHOUT_SET1_IMAGE4D_PATH]
WASHOUT_SET1_DOTS = [WASHOUT_SET1_IMAGE1_DOTS, WASHOUT_SET1_IMAGE2_DOTS, WASHOUT_SET1_IMAGE3_DOTS,
                     WASHOUT_SET1_IMAGE4_DOTS]
WASHOUT_SET2_IMAGES = [WASHOUT_SET2_IMAGE1_PATH, WASHOUT_SET2_IMAGE2_PATH, WASHOUT_SET2_IMAGE3_PATH,
                       WASHOUT_SET2_IMAGE4_PATH]
WASHOUT_SET2D_IMAGES = [WASHOUT_SET2_IMAGE1D_PATH, WASHOUT_SET2_IMAGE2D_PATH, WASHOUT_SET2_IMAGE3D_PATH,
                       WASHOUT_SET2_IMAGE4D_PATH]
WASHOUT_SET2_DOTS = [WASHOUT_SET2_IMAGE1_DOTS, WASHOUT_SET2_IMAGE2_DOTS, WASHOUT_SET2_IMAGE3_DOTS,
                     WASHOUT_SET2_IMAGE4_DOTS]


class BlockTypes(Enum):
    NEG = 1
    NEUT = 2
    POS = 3


def generate_random_numbers(total, base_value, max_diff, n=4):
    """
    Generates n random numbers between base_value and base_value+max_diff, that sums up to total
    Returns:
    A list of n numbers
    """
    increments = [random.uniform(0, max_diff) for _ in range(n-1)]

    last_value = total - sum(increments) - (base_value * (n-1))

    if base_value <= last_value <= base_value + max_diff:
        numbers = [base_value + inc for inc in increments] + [last_value]
    else:
        return generate_random_numbers(total, base_value, max_diff, n)  # Retry if out of bounds

    random.shuffle(numbers)
    return numbers


def randomize_files(directory):
    files = os.listdir(directory)
    random.shuffle(files)
    return [os.path.join(directory, file) for file in files]


class ImageRandomizer(object):
    def __init__(self, images_dir):
        self._images = randomize_files(images_dir)
        self._index = 0

    def get_images(self, number_of_images=4):
        images = self._images[self._index :self._index + number_of_images]
        self._index += number_of_images
        return images


def cv2_display_image(window_name, image, timeout_seconds):
    """
    Shows image for timeout_seconds
    """
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)

    window = tk.Tk()
    screen_width = int(window.winfo_screenwidth() * SCALE_FACTOR)
    screen_height = int(window.winfo_screenheight() * SCALE_FACTOR)
    window.destroy()

    cv2.resizeWindow(window_name, screen_width, screen_height)
    start_time = time.time()
    cv2.imshow(window_name, image)
    while time.time() - start_time < timeout_seconds:
        key = cv2.waitKey(1)
        if key == 27:
            print("ESC pressed. Exiting...")
            raise Exception("ESC pressed. Exiting...")
        time.sleep(0.01)


def cv2_display_image_with_input(window_name, image_path, timeout, specific_values=None):
    """
    Displays image_path until a user pressed a key, returns the user input as int.
    If specific_values is not None, only returns if the value pressed is in specific_values (list)
    If timeout is larger than the time passed, waits the difference and only then returns
    """

    img = cv2.imread(image_path)
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)

    window = tk.Tk()
    screen_width = int(window.winfo_screenwidth() * SCALE_FACTOR)
    screen_height = int(window.winfo_screenheight() * SCALE_FACTOR)
    window.destroy()

    cv2.resizeWindow(window_name, screen_width, screen_height)
    start_time = time.time()
    cv2.imshow(window_name, img)
    while True:
        user_input = cv2.waitKey(1)
        if user_input == 27:
            print("ESC pressed. Exiting...")
            raise Exception("ESC pressed. Exiting...")
        if specific_values is None:
            if user_input != -1:
                break
        else:
            if user_input in specific_values:
                break
        time.sleep(0.01)
    elapsed_time = time.time() - start_time
    if timeout > elapsed_time:
        time.sleep(timeout - elapsed_time)
    # Reset the keyboard buffer so if the user pressed many keys the next call for cv2.waitKey will work properly
    cv2.waitKey(1)
    return user_input


def display_image(image_path, timeout):
    """
    Shows image_path for timeout (seconds)
    """
    img = cv2.imread(image_path)
    cv2_display_image("Image", img, timeout)


def move_pointer_generator(scale, window, scale_start_time, serial_value, serial_port, lower_bound, upper_bound, timeout,
                           df_log, start_time, return_on_lock):
    def move_pointer(event):
        if event.char == "b":
            scale_value = int(scale.get())
            if scale_value > lower_bound:
                scale.set(scale_value - 1)
        elif event.char == "d":
            scale_value = int(scale.get())
            if scale_value < upper_bound:
                scale.set(scale_value + 1)
        elif event.char == "c":
            scale.config(bg="green")
            scale.config(highlightbackground='green', highlightcolor='green')
            window.update_idletasks()
            report_event(serial_port, serial_value, df_log, start_time)
            global scale_final
            scale_final = scale.get()
            if not return_on_lock:
                elapsed_time = time.time() - scale_start_time
                if timeout > elapsed_time:
                    time.sleep(timeout - elapsed_time)
            window.destroy()
    return move_pointer


def scale_timeout_generator(scale, window):
    def scale_timeout():
        global scale_final
        scale_final = scale.get()
        window.destroy()

    return scale_timeout


def close_generator(window):
    def close(event):
        window.destroy()
        print("ESC pressed. Exiting...")
        # Exceptions here don't stop the program, so we need to raise them from outside the callback
        global esc_pressed
        esc_pressed = True

    return close


def create_scale(serial_value, serial_port, scale_image_path, lower_bound, upper_bound, timeout, df_log, start_time,
                 return_on_lock=False):
    """
    Shows scale_image_path with a scale on it, scale is from lower_bound to upper_bound.
    Shows image for timeout (seconds).
    Returns the answer the user locked in (int). If user didn't lock answer before timeout, returns the current value
    of the scale.
    """
    hwnd = win32gui.FindWindow(None, "Image")
    rect = win32gui.GetWindowRect(hwnd)
    x, y, right, bottom = rect
    width = right - x
    height = bottom - y
    window = tk.Tk()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window_width = int(screen_width * SCALE_FACTOR)
    window_height = int(screen_height * SCALE_FACTOR)

    window.geometry(f"{width}x{height}+{x}+{y}")

    scale_font = font.Font(family="Helvetica", size=32, weight="bold")

    image_path = scale_image_path
    image = Image.open(image_path)
    image = image.resize((window_width, window_height))
    photo = ImageTk.PhotoImage(image)

    canvas1 = Canvas(window, width=400,
                     height=400)

    canvas1.pack(fill="both", expand=True)

    canvas1.create_image(0, 0, image=photo,
                         anchor="nw")

    # Makes so the scale is proportional to SCALE_FACTOR, places it in the lower middle part of the screen
    scale = tk.Scale(window, from_=lower_bound, to=upper_bound, orient=tk.HORIZONTAL, bd=5, length=1200*SCALE_FACTOR,
                     sliderlength=100*SCALE_FACTOR, width=50*SCALE_FACTOR, font=scale_font, tickinterval=1)
    scale.set((lower_bound + upper_bound) / 2)

    canvas1.create_window(140*SCALE_FACTOR, 400*SCALE_FACTOR,
                          anchor="nw",
                          window=scale)

    # These variables need to be edited from the bounded functions that runs as a callback when keys are pressed, so
    # they're defined as globals
    global scale_final
    scale_final = 0
    scale_start_time = time.time()

    global esc_pressed
    esc_pressed = False

    # window.bind expects a function as a second argument, to pass the current variables to that function, we use a
    # function generator that returns a function with the current variables as a parameter
    # In this case, the function moves the scale pointer, and locks in the answer when needed
    window.bind("<Key>", move_pointer_generator(scale, window, scale_start_time, serial_value, serial_port,
                                                lower_bound, upper_bound, timeout, df_log, start_time, return_on_lock))
    # In this case, the function closes the window and sets esc_pressed to true, so we know to stop the experiment
    window.bind('<Escape>', close_generator(window))
    window.focus_force()
    # Closes window after timeout and saves the current state as the answer
    window.after(timeout * 1000, scale_timeout_generator(scale, window))
    window.mainloop()

    if esc_pressed:
        raise Exception("ESC pressed. Exiting...")

    return scale_final


def washout_task(serial_port, events_encoding, set_number, df_log, start_time, df_results):
    # Uses different image set for each run
    if set_number == 1:
        images = WASHOUT_SET1_IMAGES
        images_dots = WASHOUT_SET1D_IMAGES
        dots = WASHOUT_SET1_DOTS
    else:
        images = WASHOUT_SET2_IMAGES
        images_dots = WASHOUT_SET2D_IMAGES
        dots = WASHOUT_SET2_DOTS

    # Generate a random order for the images
    indexes = list(range(4))
    random.shuffle(indexes)

    # Generate random lengths for ITI and showing image
    ITI_times = generate_random_numbers(6, 1.0, 1)
    shape_times = generate_random_numbers(10, 2.0, 1)

    for i in range(len(indexes)):
        report_event(serial_port, events_encoding["washout_task_ITI"], df_log, start_time)
        display_image(PLUS_IMAGE_PATH, ITI_times[i])

        report_event(serial_port, events_encoding["washout_task_shape"], df_log, start_time, images[indexes[i]])
        display_image(images[indexes[i]], shape_times[i])

        report_event(serial_port, events_encoding["washout_task_shape_dots"], df_log, start_time, images_dots[indexes[i]])
        display_image(images_dots[indexes[i]], 0.2)

        report_event(serial_port, events_encoding["washout_task_shape2"], df_log, start_time, images[indexes[i]])
        display_image(images[indexes[i]], 2)

        # This is so it looks better after the scale windows closes (otherwise the previous image is shown shortly)
        display_image(PLUS_IMAGE_PATH, 0.01)

        report_event(serial_port, events_encoding["washout_task_rate"], df_log, start_time)
        answer = create_scale(events_encoding["washout_task_rate_locked"], serial_port,
                     WASHOUT_SCALE_IMAGE_PATH, 0, 5, 4, df_log, start_time)

        # Log the user answers
        df_results.loc[len(df_results)] = [None, None, None, None, set_number, indexes[i],
                                           int(answer == dots[indexes[i]])]


def display_emotional_slide(block_type):
    """
    Shows the opening slide that tell what kind of pictures will be shown (NEG/NEUT/POS)
    """
    display_image(EMOTIONAL_SLIDE_PREVIEW_PATH, 4)
    if block_type == BlockTypes.NEG:
        display_image(NEG_BLOCK_START_PATH, 6)
    elif block_type == BlockTypes.NEUT:
        display_image(NEUT_BLOCK_START_PATH, 6)
    elif block_type == BlockTypes.POS:
        display_image(POS_BLOCK_START_PATH, 6)


def execute_rest(events_encoding, serial_port, rest_index, df_log, start_time, df_results):
    report_event(serial_port, events_encoding["run_rest"], df_log, start_time)
    display_image(SHORT_REST_IMAGE_PATH, 8)

    display_image(WASHOUT_START_IMAGE_PATH, 6)

    washout_task(serial_port, events_encoding, rest_index, df_log, start_time, df_results)

    report_event(serial_port, events_encoding["run_rest_2"], df_log, start_time)
    display_image(SHORT_REST_IMAGE_PATH, 10)


def execute_block(block_type, image_generator, events_encoding, serial_port, block_offset, df_log, start_time,
                  df_results, block_index, ITI_time):
    # Generate random times for displaying emotional images
    random_times = generate_random_numbers(22, 4.5, 2)
    images = image_generator.get_images()
    for i in range(len(images)):
        report_event(serial_port, events_encoding["pic_base"] + i + block_offset, df_log, start_time, images[i])
        display_image(images[i], random_times[i])

    report_event(serial_port, events_encoding["block_rest"] + block_offset, df_log, start_time)
    display_image(PLUS_IMAGE_PATH, 3)  # Rest

    report_event(serial_port, events_encoding["block_rating_neg"] + block_offset, df_log, start_time)
    emotional_scale_neg = create_scale(events_encoding["block_rating_neg_locked"] + block_offset, serial_port,
                                       EMOTIONAL_SCALE_NEG_IMAGE_PATH, 1, 7, 6,
                                       df_log, start_time)

    report_event(serial_port, events_encoding["block_rating_pos"] + block_offset, df_log, start_time)
    emotional_scale_pos = create_scale(events_encoding["block_rating_pos_locked"] + block_offset, serial_port,
                                       EMOTIONAL_SCALE_POS_IMAGE_PATH, 1, 7, 6,
                                       df_log, start_time)

    # Log the user responses
    df_results.loc[len(df_results)] = [block_type.name, block_index, emotional_scale_neg, emotional_scale_pos,
                                       None, None, None]

    report_event(serial_port, events_encoding["block_ITI"] + block_offset, df_log, start_time)
    display_image(PLUS_IMAGE_PATH, ITI_time)  # ITI


def execute_run(run_index, neg_image_generator, neut_image_generator, pos_image_generator, serial_port, subject_index):
    events_encoding = EVENTS_ENCODING

    df_log = pd.DataFrame(columns=['Time', 'Biopac', 'ImageName'])
    df_results = pd.DataFrame(columns=['BlockType', 'BlockIndex', 'NegativeEmotionalScale', 'PositiveEmotionalScale',
                                       'WashoutTaskIndex', 'WashoutImageIndex', 'IsCorrect'])

    # Shows START_IMAGE_PATH until '5' is pressed
    cv2_display_image_with_input("Image", START_IMAGE_PATH, 0, [ord('5')])
    start_time = datetime.now()

    try:
        report_event(serial_port, events_encoding["fixation_run_start"], df_log, start_time)
        display_image(PLUS_IMAGE_PATH, 8)

        # Generate random ITI times
        ITI_times = generate_random_numbers(12, 3.5, 1, 3)

        # Randomize the order of the blocks
        block_types = [(BlockTypes.NEG, neg_image_generator), (BlockTypes.NEUT, neut_image_generator),
                       (BlockTypes.POS, pos_image_generator)]
        random.shuffle(block_types)

        for i in range(len(block_types)):
            block_type, image_generator = block_types[i]
            # Set block offset for events encoding
            if block_type == BlockTypes.NEG:
                block_offset = 0
            elif block_type == BlockTypes.NEUT:
                block_offset = 20
            else:
                block_offset = 40

            report_event(serial_port, events_encoding["emotional_slide_before_images"] + block_offset, df_log, start_time)
            display_emotional_slide(block_type)

            execute_block(block_type, image_generator, events_encoding, serial_port, block_offset, df_log, start_time,
                          df_results, 1, ITI_times[i])
            execute_block(block_type, image_generator, events_encoding, serial_port, block_offset, df_log, start_time,
                          df_results, 2, ITI_times[i])
            execute_block(block_type, image_generator, events_encoding, serial_port, block_offset, df_log, start_time,
                          df_results, 3, ITI_times[i])

            # Execute rest period if not last blocks
            if i != len(block_types) - 1:
                execute_rest(events_encoding, serial_port, i + 1, df_log, start_time, df_results)

    finally:
        # Will be called either if run is finished or if esc is pressed and an exception is raised.
        # If esc is pressed, will log the answers and logs saved until that point
        start_time_str = start_time.strftime("%Y_%m_%d_%H_%M_%S")

        if not os.path.exists("data"):
            os.makedirs("data")

        # Saved dfs to data directory with unique file names for each run
        df_log.to_csv("data/WAR_LogFile_Subject_{}_Run_{}_{}.csv".format(subject_index, run_index, start_time_str))
        df_results.to_csv("data/WAR_ResultsFile_Subject_{}_Run_{}_{}.csv".format(subject_index, run_index, start_time_str))


def get_subject_index():
    """
    Opens a window to get the subject index.
    When 'Enter' is pressed the answer is submitted
    """
    window = tk.Tk()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window_width = int(screen_width * SCALE_FACTOR)
    window_height = int(screen_height * SCALE_FACTOR)

    # Create the window pinned to the upper left corner, with size SCALE_FACTOR relative from fullscreen
    window.geometry(f"{window_width}x{window_height}+0+0")

    subject_index_var = tk.StringVar()

    image = Image.open(USER_INPUT_IMAGE_PATH)
    image = image.resize((window_width, window_height))
    photo = ImageTk.PhotoImage(image)

    canvas1 = Canvas(window, width=400,
                     height=400)

    canvas1.pack(fill="both", expand=True)

    canvas1.create_image(0, 0, image=photo,
                         anchor="nw")

    # This variable needs to be edited from the submit function that runs as a callback when 'Enter' is pressed, so it's
    # defined as a global
    global subject_index
    subject_index = ""
    def submit(event):
        global subject_index
        subject_index = subject_index_var.get()

        # Close the window when answer is submitted
        window.destroy()

    name_label = tk.Label(window, text='Subject Index', font=('calibre', 20, 'bold'))

    name_entry = tk.Entry(window, textvariable=subject_index_var, font=('calibre', 20, 'normal'))

    window.bind('<Return>', submit)

    name_label.pack()
    name_entry.focus_set()
    name_entry.pack()

    global esc_pressed
    esc_pressed = False

    # window.bind expects a function as a second argument, to pass the current window to that function, we use a
    # function generator that returns a function with the current window variable as a parameter
    # In this case, the function closes the window and sets esc_pressed to true, so we know to stop the experiment
    window.bind('<Escape>', close_generator(window))
    window.mainloop()

    if esc_pressed:
        raise Exception("ESC pressed. Exiting...")

    return subject_index


def execute_experiment_opening():
    subject_index_str = get_subject_index()
    for slide in OPENING_SLIDES:
        cv2_display_image_with_input("Image", slide, 0, [ord(' ')])
    create_scale(0, None, GRID_PATH, 0, 6, 1000, None, 0, True)
    return subject_index_str


def execute_experiment():
    # Images should be random and don't repeat for whole experiment, so we randomize them here
    neg_image_generator = ImageRandomizer(NEG_IMAGES_BASE_PATH)
    neut_image_generator = ImageRandomizer(NEUT_IMAGES_BASE_PATH)
    pos_image_generator = ImageRandomizer(POS_IMAGES_BASE_PATH)
    serial_port = None
    serial_port = serial.Serial("COM1", 115200, bytesize=serial.EIGHTBITS, timeout=1)

    ctypes.windll.user32.ShowCursor(False)

    subject_index_str = execute_experiment_opening()

    execute_run(1, neg_image_generator, neut_image_generator, pos_image_generator, serial_port, subject_index_str)
    cv2_display_image_with_input("Image", LONG_REST_PATH, 0)
    execute_run(2, neg_image_generator, neut_image_generator, pos_image_generator, serial_port, subject_index_str)

    cv2_display_image_with_input("Image", END_SLIDE_PATH, 0)

    ctypes.windll.user32.ShowCursor(True)
    cv2.destroyAllWindows()


def main():
    execute_experiment()


if __name__ == "__main__":
    main()
