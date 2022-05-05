import cv2
import numpy as np
from itertools import product
from insertFlag import lsb

if __name__ == '__main__':
  flagImg=cv2.imread("out.png",1)
  sourceImg=cv2.imread("qq.jpg",1)
  for y,x in product(range(flagImg.shape[0]),range(flagImg.shape[1])):
    if (flagImg[y,x]-sourceImg[y,x]<lsb).all():
      flagImg[y,x]=np.full((3),255,np.uint8)
    else:
      flagImg[y,x]=np.full((3),0,np.uint8)
  cv2.imwrite("ans.png",flagImg)
