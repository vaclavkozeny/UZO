import cv2
import math
import numpy as np
def main():
    image = cv2.imread("/home/vaclav/GitHub/UZO/images/cv03_robot.bmp")
    image = rotate(image, 50)
    cv2.imshow("Rotated",image)
    cv2.waitKey(0)


def rotate(image, angle):
    width, height = image.shape[:2]
    center = (width // 2, height // 2)
    angle_rad = math.radians(angle)
    cos_theta = math.cos(angle_rad)
    sin_theta = math.sin(angle_rad)
    rotated_image = np.zeros((height, width, image.shape[2]), dtype=image.dtype)
    for y_new in range(height):
        for x_new in range(width):
            x_shifted = x_new - center[0]
            y_shifted = y_new - center[1]
            
            x_orig_float = x_shifted * cos_theta + y_shifted * sin_theta + center[0]
            y_orig_float = -x_shifted * sin_theta + y_shifted * cos_theta + center[1]
            
            x_orig_int = int(round(x_orig_float))
            y_orig_int = int(round(y_orig_float))
            
            if 0 <= x_orig_int < width and 0 <= y_orig_int < height:
                rotated_image[y_new, x_new] = image[y_orig_int, x_orig_int]

    return rotated_image
if __name__ == "__main__":
    main()