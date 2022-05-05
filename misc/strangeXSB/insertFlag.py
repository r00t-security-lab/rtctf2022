import cv2
from itertools import product
import numpy as np

lsb=15

if __name__ == '__main__':
  #读取图像
  flagImg=cv2.imread("flag.png",0)#黑白
  sourceImg=cv2.imread("qq.jpg",1)#彩色
  
  #使生成的flag在图像的中间
  startPoint=[(sourceImg.shape[0]-flagImg.shape[0])//2,(sourceImg.shape[1]-flagImg.shape[1])//2]
  print(flagImg.shape, sourceImg.shape, startPoint)
  for y,x in product(range(flagImg.shape[0]),range(flagImg.shape[1])):
    #如果flag图像上这个像素是黑色的, 那就把原图的这个点的所有像素值-1
    
    if flagImg[y,x]<255:
      if x<200:
        sourceImg[y+startPoint[0],x+startPoint[1]]=sourceImg[y+startPoint[0],x+startPoint[1]]&(~lsb)
      else:
        sourceImg[y+startPoint[0],x+startPoint[1]]=sourceImg[y+startPoint[0],x+startPoint[1]]^lsb
      
  #写出图像
  cv2.imwrite("out.png",sourceImg)
