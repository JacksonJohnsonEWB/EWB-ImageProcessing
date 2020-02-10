import numpy as np
from matplotlib.image import imread
from matplotlib import pyplot as plt
import matplotlib as mpl
import imageio as iio

img = imread('RoofArea2.png')

imgSize = img.shape

Hup = 240
Hlow = 120
GThresh = 100
LThresh = .5

pxCounter = 0


#print img[1908][2967]

#print type(img[1][1])

for i in range(imgSize[0]):
    for j in range(imgSize[1]):
        maxIndex = np.argmax(img[i][j][0:3])
        #print maxIndex
        if maxIndex == 0:
            Hue = (img[i][j][1]-img[i][j][2])/(max(img[i][j])-min(img[i][j]))*60
        if maxIndex == 1:
            Hue = (2+(img[i][j][2]-img[i][j][0])/(max(img[i][j])-min(img[i][j])))*60
        if maxIndex == 2:
            Hue = (4+(img[i][j][0]-img[i][j][1])/(max(img[i][j])-min(img[i][j])))*60

        Lum = (max(img[i][j][0:3])+min(img[i][j][0:3]))/2

        if Hue < Hup and Hue > Hlow and img[i][j][1] > LThresh:
            img[i][j] = [1,0,0,1]
            pxCounter = pxCounter + 1

#print pxCounter
#print img[1908][2967]
#print img.shape

iio.imwrite('RoofSelectorOut.png',img)

