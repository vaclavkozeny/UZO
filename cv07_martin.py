import cv2
import math
import numpy as np

class Node:
    def __init__(self,id_num):
        self.id_num=id_num
    def __hash__(self):
        return self.id_num
    def __eq__(self, other):
        return self.id_num == other.id_num


def segment(image):
    R = image[:,:,2].astype(float)
    G = image[:,:,1].astype(float)
    B = image[:,:,0].astype(float)
    g = (G * 255) / (R + G + B)
    threshold = 105
    filtered = (g < threshold).astype(np.uint8)
    return filtered

def  identification(image):
    arr=np.full(image.shape, None)
    cnt=0
    block_size = 3
    offsetx=1
    offsety=1
    for i in range(image.shape[0]-2):
        for j in range(image.shape[1]-2):
            block = arr[i:i + block_size, j:j + block_size]
            center = block[1][1]
            center_img_val=image[i+1,j+1]
            neighbors = [
                arr[i + di][j + dj]
                for di in range(3)
                for dj in range(3)
                if not (di == 1 and dj == 1)
            ]
            if center is None and center_img_val >= 0.9:
                nodes = [n for n in neighbors if n is not None]
                nodes_set=set(nodes)
                if len(nodes)==0:
                    cnt = cnt + 1
                    arr[i +offsetx][j+offsety ] = Node(cnt)
                    continue
                if len(nodes)==1 or len(nodes_set)==1:
                    arr[i +offsetx][j+offsety ] = nodes[0]
                    continue
                if len(nodes)>=2 and len(nodes_set)>=2:
                    arr[i +offsetx][j+offsety ] = nodes[0]
                    for node in list(nodes_set):
                        node.id_num = nodes[0].id_num
                    continue
    return arr

def convert_to_num(image):
    arr=np.full(image.shape, 0)
    for i in range(0, arr.shape[0], 1):
        for j in range(0, arr.shape[1], 1):
            if image[i,j] is not None:
                arr[i,j] = image[i,j].id_num
            else:
                arr[i,j] = 0
    return arr

def mass(arr):
    vals=np.unique(arr)
    for v in vals:
        if v ==0:
            continue
        x=0
        y=0
        cnt=0
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                if arr[i,j] == v:
                    x=x+i
                    y=y+j
                    cnt=cnt+1
        vysl="1"
        if cnt>=4000:
            vysl="5"
        x=x/cnt
        y=y/cnt
        print("Souřadnice X:"+str(x),",Y:"+str(y)+", mince:"+vysl)

if __name__ == "__main__":
    image = cv2.imread(".img/cv07_segmentace.bmp")
    segm_image=segment(image)#*255
    iden_arr=identification(segm_image)
    mass(convert_to_num(iden_arr))
    input()