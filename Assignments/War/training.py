from WAR_main import cv2_display_image_with_input, create_scale, GRID_PATH, show_background
import ctypes
import cv2


def training():
    cv2_display_image_with_input("Image", GRID_PATH, 0, [ord('5')])
    create_scale(0, None, GRID_PATH, 0, 6, 1000, None, 0, True)


def main():
    ctypes.windll.user32.ShowCursor(False)
    show_background()

    training()

    ctypes.windll.user32.ShowCursor(True)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
