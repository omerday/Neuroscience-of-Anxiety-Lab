from WAR_main import cv2_display_image_with_input, display_image, PLUS_IMAGE_PATH, show_background
from serialHandler import EVENTS_ENCODING, report_event
import ctypes
import cv2
import serial

BASELINE_INSTRUCTIONS_PATH = "WAR_images/Utils/BaselineInstructions.jpg"


def baseline():
    ctypes.windll.user32.ShowCursor(False)
    show_background()

    serial_port = None
    serial_port = serial.Serial("COM1", 115200, bytesize=serial.EIGHTBITS, timeout=1)
    cv2_display_image_with_input("Image", BASELINE_INSTRUCTIONS_PATH, 0, [ord('5')])
    report_event(serial_port, EVENTS_ENCODING['baseline_start'], None, 0)
    display_image(PLUS_IMAGE_PATH, (8 * 60) + 12)

    ctypes.windll.user32.ShowCursor(True)
    cv2.destroyAllWindows()


def main():
    baseline()


if __name__ == "__main__":
    main()
