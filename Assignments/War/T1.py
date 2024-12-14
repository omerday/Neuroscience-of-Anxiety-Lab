from WAR_main import (cv2_display_image_with_input, display_image, PLUS_IMAGE_PATH, show_background,
                      create_anxiety_scale, get_subject_index, SESSION_INPUT_IMAGE_PATH)
from training import training
from serialHandler import EVENTS_ENCODING, report_event
import pandas as pd
from datetime import datetime
import ctypes
import cv2
import serial

T1_INSTRUCTIONS_PATH = "WAR_images/Utils/T1Instructions.jpg"


def T1():
    ctypes.windll.user32.ShowCursor(False)
    show_background()

    display_image(PLUS_IMAGE_PATH, 0)
    subject_index = get_subject_index()
    session_index = get_subject_index(SESSION_INPUT_IMAGE_PATH)

    training()

    serial_port = None
    serial_port = serial.Serial("COM1", 115200, bytesize=serial.EIGHTBITS, timeout=1)

    df_results = pd.DataFrame(columns=['SubjectIndex', 'SessionIndex', 'ExperimentName', 'AnxietyLevel'])

    anxiety_level = create_anxiety_scale()
    df_results.loc[len(df_results)] = [subject_index, session_index, "T1", anxiety_level]

    df_results.to_csv("data/WAR_ResultsFile_T1_Subject_{}_Session_{}_{}.csv".format(subject_index,
                                                                                          session_index,
                                                                                          datetime.now().strftime(
                                                                                              "%Y_%m_%d_%H_%M_%S")))

    cv2_display_image_with_input("Image", T1_INSTRUCTIONS_PATH, 0, [ord('5')])
    report_event(serial_port, EVENTS_ENCODING['T1_start'], None, 0)
    display_image(PLUS_IMAGE_PATH, 5 * 60)

    ctypes.windll.user32.ShowCursor(True)
    cv2.destroyAllWindows()


def main():
    T1()


if __name__ == "__main__":
    main()
