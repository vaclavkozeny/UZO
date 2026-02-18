import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
plt.ion()
clear = lambda: os.system('cls')
clear()
plt.close('all')

cap = cv2.VideoCapture('cv02/cv02_hrnecek.mp4')
template = cv2.imread("cv02/cv02_vzor_hrnecek.bmp")
hsv_t = cv2.cvtColor(template, cv2.COLOR_RGB2HSV)
hist_t, b_t = np.histogram(hsv_t[:,:,0], 256, (0, 256))
hist_t = np.divide(hist_t,max(hist_t))
hist_t = np.where(hist_t < 0.75, 0, hist_t)

x1 = 100
y1 = 100
x2 = 200
y2 = 200
new_array = np.zeros((480,640))
while True:
    ret, bgr = cap.read()
    if not ret:
        break
    hsv = cv2.cvtColor(bgr, cv2.COLOR_RGB2HSV)
    hist, b = np.histogram(hsv[:,:,0], 256, (0, 256))
    new_array = hist_t[hsv[...,0]]

    new_array = np.array(new_array)
    x, y = np.indices(new_array.shape)  # pozor: y = řádky, x = sloupce

    # vážené souřadnice
    t_x = np.sum(x * new_array)
    t_y = np.sum(y * new_array)

    total = np.sum(new_array)

    tez_x = int(t_x / total)
    tez_y = int(t_y / total)

    cv2.rectangle(bgr, (tez_y-50, tez_x-100), (tez_y + 50, tez_x + 100), (0, 255, 0))
    cv2.imshow('Image', bgr)
    key = 0xFF & cv2.waitKey(30)
    if key == 27:
        break
    
cv2.destroyAllWindows()

