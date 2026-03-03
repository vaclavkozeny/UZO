import cv2
import math
import numpy as np
def main():
    image = cv2.imread("images/cv03_robot.bmp")
    cv2.imshow("",image)
    cv2.waitKey()
    image = rotate(image, 0)
    cv2.imshow("",image)
    cv2.waitKey()

def getRotationMatrix2D(center,angle):
    x,y = center
    # math.sin/cos počítá se uhlem v radianech
    angle=math.radians(angle)
    movetocenter=\
        [[1,0,x],
         [0,1,y],
         [0,0,1]]
    rotatematrix=\
        [[math.cos(angle),math.sin(angle),0],
         [-math.sin(angle),math.cos(angle),0],
         [0,0,1]]
    moveback = \
        [[1, 0, -x],
         [0, 1, -y],
         [0, 0, 1]]
    r=np.dot(np.dot(movetocenter,rotatematrix),moveback)
    return r[:-1,:]
def rotate(image, angle):
    width, height = image.shape[:2]
    center = (width // 2, height // 2)
    #print(image)
    #print(cv2.getRotationMatrix2D(center, angle,1))
    #print(getRotationMatrix2D(center, angle))
    rotation_mat=getRotationMatrix2D(center, angle)
    # rotation calculates the cos and sin, taking absolutes of those.
    abs_cos = abs(rotation_mat[0, 0])
    abs_sin = abs(rotation_mat[0, 1])

    # find the new width and height bounds
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    # subtract old image center (bringing image back to origo) and adding the new image center coordinates
    # bound_w / 2 - center[0] rozdíl mezi středem původního obrázku a
    # středem nového většího obrázku, vzniklém otočením
    rotation_mat[0, 2] += bound_w / 2 - center[0]
    rotation_mat[1, 2] += bound_h / 2 - center[1]
    return manual_warpAffine(image, np.array(rotation_mat), (bound_w, bound_h))

def manual_warpAffine(image, M, size):
    h, w = size
    new_image = np.zeros((h, w, 3), dtype=image.dtype)
    M_inv = np.linalg.inv(np.vstack([M, [0,0,1]]))[:2,:]
    for y in range(h):
        for x in range(w):
            src = np.dot(M_inv, [x, y, 1])
            src_x, src_y = int(round(src[0])), int(round(src[1]))
            if 0 <= src_x < image.shape[1] and 0 <= src_y < image.shape[0]:
                new_image[y, x] = image[src_y, src_x]

    return new_image
if __name__ == "__main__":
    main()