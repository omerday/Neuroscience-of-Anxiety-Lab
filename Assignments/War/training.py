from WAR_main import cv2_display_image_with_input, create_scale
import ctypes
import cv2

GRID_PATH = "WAR_images/Utils/Grid.jpg"


def training():
    ctypes.windll.user32.ShowCursor(False)

    cv2_display_image_with_input("Image", GRID_PATH, 0, [ord('5')])
    create_scale(0, None, GRID_PATH, 0, 6, 1000, None, 0, True)

    ctypes.windll.user32.ShowCursor(True)
    cv2.destroyAllWindows()


def main():
    training()


if __name__ == "__main__":
    main()
