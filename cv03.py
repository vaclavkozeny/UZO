import cv2
import math
import numpy as np
def main():
    image = cv2.imread("/home/vaclav/GitHub/UZO/images/cv03_robot.bmp")
    image = rotate(image, 45)
    cv2.imshow(image)


def rotate(image, angle):
    width, height = image.shape[:2]
    center = (width // 2, height // 2)
    print(image)
    print(cv2.getRotationMatrix2D(center, angle, 1))
    rotation_matrix = [[math.cos(angle),-math.sin(angle)],[math.sin(angle), math.cos(angle)]]
    print(rotation_matrix)
    return cv2.warpAffine(image, np.array(rotation_matrix), (width, height))

if __name__ == "__main__":
    main()