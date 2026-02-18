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
x1 = 100
y1 = 100
x2 = 200
y2 = 200
new_array = np.zeros((640,480))
while True:
    ret, bgr = cap.read()
    if not ret:
        break
    hsv = cv2.cvtColor(bgr, cv2.COLOR_RGB2HSV)
    hist, b = np.histogram(hsv[:,:,0], 256, (0, 256))
    for x in range(len(new_array)):
        for y in range(len(new_array[0])):
            new_array[x][y] = hist_t[hsv[y][x][0]]
    new_array = np.array(new_array)
    t_x = 0
    t_y = 0
    for x in range(len(new_array)):
        for y in range(len(new_array[0])):
            t_x = t_x + x*new_array[x][y]
            t_y = t_y + y*new_array[x][y]
    tez_x = int(t_x/np.sum(new_array))
    tez_y = int(t_y/np.sum(new_array))

    cv2.rectangle(bgr, (tez_x-50, tez_y-100), (tez_x + 50, tez_y + 100), (0, 255, 0))
    cv2.imshow('Image', bgr)
    key = 0xFF & cv2.waitKey(30)
    if key == 27:
        break
    
cv2.destroyAllWindows()

