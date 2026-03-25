import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import dctn, idctn 

def main():
    image = cv2.imread("images/cv04c_robotC.bmp", cv2.IMREAD_GRAYSCALE)
    mask = cv2.imread("images/cv04c_filtHP.bmp",cv2.IMREAD_GRAYSCALE)
    #plt.imshow(np.log(np.abs(dft_2d(image))))
    #plt.imshow(np.log(np.abs(dct(image))),cmap='jet')
    plt.imshow(dct_reduced(image,30), cmap='gray')
    #plt.imshow(apply_mask(image,mask),cmap='gray')
    plt.show()

def dft_2d(image):
    fft2 = np.fft.fft2(image)
    return shift_spectrum(fft2)

def shift_spectrum(fftS):
    return np.fft.fftshift(fftS)

def dct(image):
    image = np.float32(image)
    return dctn(image)

def dct_reduced(image, size):
    dctS = dct(image)
    dct_truncated = np.zeros_like(dctS)
    dct_truncated[0:size, 0:size] = dctS[0:size, 0:size]
    return idctn(dct_truncated)

def apply_mask(image,mask):
    mask = (mask > 127).astype(np.float32)
    fft2 = dft_2d(image)
    filtered = fft2*mask
    filtered = np.fft.ifftshift(filtered)
    return np.abs(np.fft.ifft2(filtered))


if __name__ == "__main__":
    main()