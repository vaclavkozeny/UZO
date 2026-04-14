
import cv2
import numpy as np
import os

def main():
    #Trénování
    Wp=ImageMatrix()
    wp=np.mean(Wp, axis=1)
    W=Wp-wp
    C=np.dot(W.transpose()*W)
    D, Ep = np.linalg.eig(C)  # E eigenvectors, D eigenvalues

    idx = np.argsort(D)[::-1]  # indexy seřazené od největšího vlastního čísla
    D = D[idx]  # seřazená vlastní čísla
    Ep = Ep[:, idx]

    E=np.dot(W,Ep)
    PI=np.dot(E.transpose(),W)

    #Testoací část
    path=""
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    wpu=img.flatten()
    wu=wpu-wp
    PT=np.dot(E.transpose(),wu)

    n = PI.shape[1]  # počet známých vzorů
    distances = np.zeros(n)

    for i in range(n):
        diff = PI[:, i] - PT                  # rozdíl vektorů
        distances[i] = np.sqrt(np.sum(diff**2))  # euklidovská vzdálenost

    np.argmin(distances)  # index nejbližšího vzoru

    return


def ImageMatrix(folderAdd: str) -> np.ndarray:
    files = [f for f in os.listdir(folderAdd)]

    columns = []

    for filename in files:
        path = os.path.join(folderAdd, filename)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        col = img.flatten()
        columns.append(col)

    matrix = np.column_stack(columns)   # tvar (W*H, počet_obrázků)
    return matrix



if __name__ == '__main__':
    main()