import cv2
from matplotlib import pyplot as plt
import numpy as np
from scipy.signal import find_peaks

def main():
    img = cv2.imread("images/cv07_segmentace.bmp")
    #segmentace(img)
    barveni()

def segmentace(img):
    R = img[:,:,2].astype(float)
    G = img[:,:,1].astype(float)
    B = img[:,:,0].astype(float)

    g = (G * 255)/(R+G+B)
    threshold = 105
    """
    hist = plt.hist(g.ravel(), 256)
    print(hist)
    threshold = find_peaks(hist)
    print(threshold)
    """
    mask = (g < threshold).astype(np.uint8) * 255
    return mask

def barveni():
    img = cv2.imread("images/cv07_barveni.bmp", cv2.IMREAD_GRAYSCALE)
    rows, cols = img.shape
    colors = np.zeros_like(img)
    counter = 2
    zones = {}
    for i in range(rows):
        for j in range(cols):
            if img[i][j] == 0:
                continue
            neighbour_vals = set()
            if j > 0:
                neighbour_vals.add(colors[i][j-1])
            if i > 0 and j > 0:
                neighbour_vals.add(colors[i-1][j-1])
            if i > 0:
                neighbour_vals.add(colors[i-1][j])
            if i > 0 and j < cols-1:
                neighbour_vals.add(colors[i-1][j+1])

            neighbour_vals.discard(0)
            if len(neighbour_vals) == 0:
                colors[i][j] = counter
                zones[counter] = set()
                counter += 1
            else:
                min_label = min(neighbour_vals)
                colors[i][j] = min_label
                for lbl in neighbour_vals:
                    if lbl != min_label:
                        zones[lbl] = min_label
    for i in range(rows):
        for j in range(cols):
            zone = colors[i][j]
            if zone == 0:
                continue
            root = zone
            while zones[root] != root:
                root = zones[root]
            colors[i][j] = root
            

if __name__ ==  "__main__":
    main()