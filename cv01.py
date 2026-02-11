import cv2
from matplotlib import pyplot as plt
import numpy as np

def main():
    data = []
    for i in range(1,10):
        row_data = []
        patern = path_to_hist(f"./images/im0{i}.jpg")
        for j in range(1,10):
            to_compare = path_to_hist(f"./images/im0{j}.jpg")
            row_data.append({"image":j,"value":calculate(patern, to_compare)})
        data.append(row_data)
    print(data)
    draw_image(data)

def path_to_hist(path:str):
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    return cv2.calcHist([image],[0],None,[256],[0,256])

def calculate(source, compare):
    source = np.array(source)
    compare = np.array(compare)
    res = np.absolute(np.subtract(source, compare))
    return np.sum(res)
def draw_image(data):
    counter = 1
    for i in range(len(data)):
        sorted_data = sorted(data[i],key=lambda x: x["value"])
        for j in range(len(data[i])):
            plt.subplot(9,9,counter)
            counter += 1
            plt.imshow(cv2.cvtColor(cv2.imread(f"./images/im0{sorted_data[j]["image"]}.jpg"),cv2.COLOR_BGR2RGB))
            plt.xticks([])
            plt.yticks([])
    plt.savefig("images.png")

if __name__ ==  "__main__":
    main()