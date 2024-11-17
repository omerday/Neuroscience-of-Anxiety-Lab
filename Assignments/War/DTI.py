from WAR_main import cv2_display_image_with_input, display_image, PLUS_IMAGE_PATH, START_IMAGE_PATH, SCALE_FACTOR
from serialHandler import EVENTS_ENCODING, report_event
import ctypes
import cv2
import tkinter as tk
import serial

DTI_INSTRUCTIONS_PATH = "WAR_images/Utils/DTIInstructions.jpg"
VIDEO_PATH = ""  # TODO: Fill after video found


def show_video(video_path):
    window = tk.Tk()
    screen_width = int(window.winfo_screenwidth() * SCALE_FACTOR)
    screen_height = int(window.winfo_screenheight() * SCALE_FACTOR)
    window.destroy()

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    while cap.isOpened():
        ret, frame = cap.read()  # Capture frame-by-frame
        if not ret:
            print("Reached end of video or cannot fetch the frame.")
            break

        cv2.namedWindow('Image', cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
        cv2.resizeWindow('Image', screen_width, screen_height)
        cv2.imshow('Image', frame)

        # Break the loop if the user presses the ESC key
        if cv2.waitKey(25) & 0xFF == 27:
            break

    cap.release()


def DTI():
    ctypes.windll.user32.ShowCursor(False)

    serial_port = None
    serial_port = serial.Serial("COM1", 115200, bytesize=serial.EIGHTBITS, timeout=1)
    user_input = cv2_display_image_with_input("Image", DTI_INSTRUCTIONS_PATH, 0, [ord('b'), ord('c')])

    if user_input == ord('b'):  # Fixation
        cv2_display_image_with_input("Image", START_IMAGE_PATH, 0, [ord('5')])
        report_event(serial_port, EVENTS_ENCODING['DTI_fixation_start'], None, 0)
        display_image(PLUS_IMAGE_PATH, 15 * 60)
    else:
        cv2_display_image_with_input("Image", START_IMAGE_PATH, 0, [ord('5')])
        report_event(serial_port, EVENTS_ENCODING['DTI_video_start'], None, 0)
        show_video(VIDEO_PATH)

    ctypes.windll.user32.ShowCursor(True)
    cv2.destroyAllWindows()


def main():
    DTI()


if __name__ == "__main__":
    main()
