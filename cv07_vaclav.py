import cv2
from matplotlib import pyplot as plt
import numpy as np
from scipy.signal import find_peaks

def main():
    img_o = cv2.imread("images/cv07_segmentace.bmp")
    img = segmentace(img_o)
    img, roots = barveni(img)
    #barveni(img)
    tez = teziste(img, roots)
    print(tez)
    print(soucet_hodnot(tez))
    plt.imshow(hodnota_do_obrazku(teziste_do_obrazku(img_o, tez), tez))
    plt.show()

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
    mask = (g < threshold).astype(np.uint8)
    return mask

def barveni(img):
    #img = cv2.imread("images/cv07_barveni.bmp", cv2.IMREAD_GRAYSCALE)
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
                counter += 1
            else:
                min_label = min(neighbour_vals)
                colors[i][j] = min_label
                for lbl in neighbour_vals:
                    if lbl != min_label:
                        zones[min_label] = lbl
    sets = []
    for u, v in zones.items():
        found_in_set = []
        for s in sets:
            if u in s or v in s:
                found_in_set.append(s)
        if len(found_in_set) == 0:
            sets.append({u, v})
        elif len(found_in_set) == 1:
            found_in_set[0].add(u)
            found_in_set[0].add(v)
        #spojeni dvou mnozin
        else: 
            merged_set = set()
            for s in found_in_set:
                merged_set.update(s)
                sets.remove(s)
            merged_set.add(u)
            merged_set.add(v)
            sets.append(merged_set)
    label_mapping = {}
    unique_colors = set()
    for s in sets:
        min_val = min(s)
        for val in s:
            label_mapping[val] = min_val
            unique_colors.add(min_val)
    for i in range(rows):
        for j in range(cols):
            val = colors[i][j]
            if val != 0:
                new_val = label_mapping.get(val,val)
                colors[i][j] = new_val
    return colors, unique_colors
def teziste(img, colors):
    tez = {}
    for i in colors:
        maska = (img == i).astype(np.uint8)
        M = cv2.moments(maska)
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        tez[int(i)] = {"teziste":(cx,cy), "hodnota":5 if M["m00"] > 4000 else 1}
    return tez
def teziste_do_obrazku(img, tez):
    for _, value in tez.items():
        cx, cy = value["teziste"]
        cv2.circle(img, (cx, cy), 3, (0, 0, 255), -1)
    return img
def hodnota_do_obrazku(img, tez):
    for _, value in tez.items():
        cx, cy = value["teziste"]
        hodnota = value["hodnota"]
        cv2.putText(img, str(hodnota), (cx+5, cy-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
    return img
def soucet_hodnot(tez):
    total = 0
    for _, value in tez.items():
        total += value["hodnota"]
    return total

if __name__ ==  "__main__":
    main()