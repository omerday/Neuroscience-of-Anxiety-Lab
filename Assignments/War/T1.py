from WAR_main import cv2_display_image_with_input, display_image, PLUS_IMAGE_PATH
from serialHandler import FIRST_RUN_EVENTS_ENCODING, report_event
import ctypes
import cv2

T1_INSTRUCTIONS_PATH = "WAR_images/Utils/T1Instructions.jpg"


def T1():
    ctypes.windll.user32.ShowCursor(False)

    serial_port = None
    # serial_port = serial.Serial("COM1", 115200, bytesize=serial.EIGHTBITS, timeout=1)
    cv2_display_image_with_input("Image", T1_INSTRUCTIONS_PATH, 0, [ord('5')])
    report_event(serial_port, FIRST_RUN_EVENTS_ENCODING['T1_start'], None, 0)
    display_image(PLUS_IMAGE_PATH, 5 * 60)

    ctypes.windll.user32.ShowCursor(True)
    cv2.destroyAllWindows()
    
def main():
    T1()


if __name__ == "__main__":
    main()
