import cv2
import matplotlib.pyplot as plt
import numpy as np


avg_kernel =    [[1/9,1/9,1/9],

                [1/9,1/9,1/9],

                [1/9,1/9,1/9]]

def main():
    img = cv2.imread("images/cv05_robotS.bmp",cv2.IMREAD_GRAYSCALE)
    filtered_avg = apply_convolution(img,avg_kernel)
    filtered_mask = rotating_mask_filter(img)
    filtered_med = conv_median(img)
    plt.subplot(4,2,1)
    plt.imshow(img, cmap="gray")
    plt.subplot(4,2,2)
    c_img = plt.imshow(np.log(np.abs(dft_2d(img))),cmap="jet")
    plt.colorbar(c_img)
    plt.subplot(4,2,3)
    plt.imshow(filtered_med, cmap="gray")
    plt.title = "median"
    plt.subplot(4,2,4)
    c_median = plt.imshow(np.log(np.abs(dft_2d(filtered_med))),cmap="jet")
    plt.colorbar(c_median)
    plt.subplot(4,2,5)
    plt.imshow(filtered_avg, cmap="gray")
    plt.subplot(4,2,6)
    c_avg = plt.imshow(np.log(np.abs(dft_2d(filtered_avg))),cmap="jet")
    plt.colorbar(c_avg)
    plt.subplot(4,2,7)
    plt.imshow(filtered_mask, cmap="gray")
    plt.subplot(4,2,8)
    c_mask = plt.imshow(np.log(np.abs(dft_2d(filtered_mask))),cmap="jet")
    plt.colorbar(c_mask)
    plt.savefig("cv05.png")
    plt.show()


def dft_2d(image):
    fft2 = np.fft.fft2(image)
    return shift_spectrum(fft2)

def shift_spectrum(fftS):
    return np.fft.fftshift(fftS)

def rotating_mask_filter(img):
    pad = 2
    img_padded = np.pad(img, pad, mode='edge').astype(np.float32)
    rows, cols = img.shape
    result = np.zeros_like(img_padded)
    offsets = [
        (-2,-2), (-2,-1), (-2, 0),
        (-1,-2),          (-1, 0),
        ( 0,-2), ( 0,-1), ( 0, 0)
    ]
    for x in range(pad, rows + pad):
        for y in range(pad, cols + pad):
            best_var = float('inf')
            best_mean = 0
            for offx, offy in offsets:
                window = img_padded[x+offx : x+offx+3, y+offy : y+offy+3]
                var = np.var(window)
                if var < best_var:
                    best_var = var
                    best_mean = np.mean(window)
            result[x, y] = best_mean
    return result[pad:-pad, pad:-pad].astype(np.uint8)


def conv_median(img):
    rows, cols = img.shape
    result = np.zeros_like(img)
    for x in range(1, rows + 1):
        for y in range(1, cols + 1):
            window = img[x-1 : x+1, y-1 : y+1]
            result[x-1,y-1] = np.median(window)
    return result

def apply_convolution(img, kernel):
    kernel = np.array(kernel, dtype=np.float32)
    result = cv2.filter2D(img, -1, kernel)
    return result

if __name__ ==  "__main__":
    main()