from WAR_main import cv2_display_image_with_input, display_image, GRID_PATH, create_scale


def training():
    cv2_display_image_with_input("Image", GRID_PATH, 0, ord('5'))
    create_scale(0, None, GRID_PATH, 0, 6, 1000, None, 0, True)


def main():
    training()


if __name__ == "__main__":
    main()
