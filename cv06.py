import cv2
import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss


def laplacian(image) :
    matrix=np.array(
        [
            [1,1,1],
            [1,-8,1],
            [1,1,1]
        ]
    )
    return cv2.filter2D(image, cv2.CV_64F, matrix)
"""
def sobel(image) :
    matrix = np.array([
        [1,2,1],
        [0 ,0 ,0],
        [-1,-2,-1]
    ])
    matrix2 = np.array([
        [0, 1, 2],
        [-1, 0, 1],
        [-2, -1, 0]
    ])
    h=[matrix,matrix2]
    new_image=np.full_like(image)
    for x in range(3):
        matrix=np.rot90(matrix)
        h.append(matrix)
        matrix2=np.rot90(matrix2)
        h.append(matrix2)
    for i in range(0,len(image)-2):
        for j in range(0,len(image[0])-2):
            block = [
                row[j:j + 3]
                for row in image[i:i + 3]
            ]
            block=np.array(block)
            max=0
            for mask in h:
                val=ss.convolve2d(block, mask, "valid")[0]
                if val> max:
                    max=val
            new_image[i+1][j+1] = max
    return new_image
"""
def sobel(image) :
    matrix = np.array([
        [1,2,1],
        [0 ,0 ,0],
        [-1,-2,-1]
    ])
    matrix2 = np.array([
        [0, 1, 2],
        [-1, 0, 1],
        [-2, -1, 0]
    ])
    h=[matrix,matrix2]
    for x in range(3):
        matrix=np.rot90(matrix)
        h.append(matrix)
        matrix2=np.rot90(matrix2)
        h.append(matrix2)
    result=np.zeros_like(image)
    for mask in h:
            a=cv2.filter2D(image, cv2.CV_64F, mask)
            result=np.maximum(result, a)
    return result

def kirk(image) :
    matrix = np.array([
        [3,3,3],
        [3,0 ,3],
        [-5,-5,-5]
    ])
    matrix2 = np.array([
        [3, 3, 3],
        [-5, 0, 3],
        [-5, -5, 3]
    ])
    h=[matrix,matrix2]
    for x in range(3):
        matrix=np.rot90(matrix)
        h.append(matrix)
        matrix2=np.rot90(matrix2)
        h.append(matrix2)
    result=np.zeros_like(image)
    for mask in h:
            result=np.maximum(result, cv2.filter2D(image, cv2.CV_64F, mask))
    return result

def spectum(image) :
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    plt.imshow(np.log(np.abs(fshift)), cmap="jet")
    plt.colorbar()

if __name__ == "__main__":
    image = cv2.imread("images/cv06_robotC.bmp")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    plt.figure(constrained_layout=True, figsize=(12, 10))
    plt.subplot(421)
    plt.imshow(image, cmap="gray")
    plt.colorbar()

    plt.subplot(422)
    spectum(image)

    plt.subplot(423)
    lap=laplacian(image)
    plt.imshow(lap,cmap="jet")
    plt.colorbar()

    plt.subplot(424)
    spectum(lap)

    plt.subplot(425)
    sob=sobel(image)
    plt.imshow(sob, cmap="jet")
    plt.colorbar()

    plt.subplot(426)
    spectum(sob)

    plt.subplot(427)
    kirk = kirk(image)
    plt.imshow(kirk, cmap="jet")
    plt.colorbar()

    plt.subplot(428)
    spectum(kirk)
    plt.show()
