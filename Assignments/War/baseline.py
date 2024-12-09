from WAR_main import (cv2_display_image_with_input, display_image, PLUS_IMAGE_PATH, show_background,
                      create_anxiety_scale, get_subject_index, SESSION_INPUT_IMAGE_PATH)
from serialHandler import EVENTS_ENCODING, report_event
import pandas as pd
import ctypes
import cv2
from datetime import datetime
import serial

BASELINE_INSTRUCTIONS_PATH = "WAR_images/Utils/BaselineInstructions.jpg"


def baseline():
    ctypes.windll.user32.ShowCursor(False)
    show_background()

    serial_port = None
    serial_port = serial.Serial("COM1", 115200, bytesize=serial.EIGHTBITS, timeout=1)

    df_results = pd.DataFrame(columns=['SubjectIndex', 'SessionIndex', 'ExperimentName', 'AnxietyLevel'])

    display_image(PLUS_IMAGE_PATH, 0)

    subject_index = get_subject_index()
    session_index = get_subject_index(SESSION_INPUT_IMAGE_PATH)
    anxiety_level = create_anxiety_scale()
    df_results.loc[len(df_results)] = [subject_index, session_index, "Baseline", anxiety_level]

    df_results.to_csv("data/WAR_ResultsFile_Baseline_Subject_{}_Session_{}_{}.csv".format(subject_index,
                                                        session_index, datetime.now().strftime("%Y_%m_%d_%H_%M_%S")))

    cv2_display_image_with_input("Image", BASELINE_INSTRUCTIONS_PATH, 0, [ord('5')])
    report_event(serial_port, EVENTS_ENCODING['baseline_start'], None, 0)
    display_image(PLUS_IMAGE_PATH, (8 * 60) + 12)

    ctypes.windll.user32.ShowCursor(True)
    cv2.destroyAllWindows()


def main():
    baseline()


if __name__ == "__main__":
    main()
