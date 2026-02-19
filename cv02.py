import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
plt.ion()
clear = lambda: os.system('cls')
clear()
plt.close('all')

cap = cv2.VideoCapture('/home/vaclav/GitHub/UZO/images/cv02_hrnecek.mp4')
template = cv2.imread("/home/vaclav/GitHub/UZO/images/cv02_vzor_hrnecek.bmp")
template_h, template_w = template.shape[:2]
hsv_t = cv2.cvtColor(template, cv2.COLOR_RGB2HSV)   
hist = cv2.calcHist([hsv_t],[0],None,[180],[0, 180])
cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
x1 = y1 = x2 = y2 = None
while True:
    ret, bgr = cap.read()
    if not ret:
        break
    hsv = cv2.cvtColor(bgr, cv2.COLOR_RGB2HSV)
    hsv_h, hsv_w = hsv.shape[:2]
    if x1 is not None:
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(hsv_w, x2)
        y2 = min(hsv_h, y2)
        hsv = hsv[y1:y2, x1:x2]
        offset_x = x1
        offset_y = y1
    else:
        offset_x = 0
        offset_y = 0
    bp = cv2.calcBackProject([hsv], [0], hist, [0, 180], 1)
    #_, filtered_bp = cv2.threshold(bp, 200, 255, cv2.THRESH_BINARY)
    M = cv2.moments(bp)
    tez_x = int(M["m10"] / M["m00"]) + offset_x
    tez_y = int(M["m01"] / M["m00"]) + offset_y
    x1 = int(tez_x - template_w/2)
    y1 = int(tez_y - template_h/2)
    x2 = int(tez_x + template_w/2)
    y2 = int(tez_y + template_h/2)
    cv2.rectangle(bgr, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.imshow('Image', bgr)
    key = 0xFF & cv2.waitKey(30)
    if key == 27:
        break
    
cv2.destroyAllWindows()

