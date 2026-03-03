import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import dctn, idctn 

def main():
    image = cv2.imread("images/cv04c_robotC.bmp")
    #plt.imshow(np.log(np.abs(dft_2d(image))+1))
    #plt.imshow(np.log(np.abs(dct(image))+1))
    plt.imshow(dct_reduced(image,50), cmap='gray')
    
    plt.show()

def dft_2d(image):
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fft2 = np.fft.fft2(image)
    return shift_spectrum(fft2)

def shift_spectrum(fftS):
    return np.fft.fftshift(fftS)

def dct(image):
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = np.float32(image)
    return dctn(image,norm='ortho')

def dct_reduced(image, size):
    dctS = dct(image)
    dct_truncated = np.zeros_like(dctS)
    dct_truncated[0:size, 0:size] = dctS[0:size, 0:size]
    return idctn(dct_truncated, norm='ortho')

if __name__ == "__main__":
    main()