#Jackson Johnson
#Written for the Hartford Proffession Chapter of EWB-USA
#January 2020
#jackson.david.johnson@gmail.com

#Sentinel Hyperspectral Processor (SHP). computes the Normalized Diference Vegitation Index (NDVI) 
#and a Moisture Index from given Infra Red Data. These use specific Sentinel-2 satellite bands. 
#Other IR sources (like landsat) can be used, just make sure the wavelengths line up.

import numpy as np
from matplotlib.image import imread
import matplotlib.pyplot as plt
import imageio as iio



#Read in the images. If anybody knows how to read these in as floats and not unsigned 
#integers that come in as, I would be greatful to hear about it. Failure to convert from
#unsigned integers results in underflow errors. If the whole array could be converted 
#into floats at once, there is probably a 25x speed increase opportunity.
B8A = imread('T37MBQ_20200104T074311_B8A.jp2')
B11 = imread('T37MBQ_20200104T074311_B11.jp2')
B8 =  imread('T37MBQ_20200104T074311_B08.jp2')
B4 =  imread('T37MBQ_20200104T074311_B04.jp2') #Red Color channel


#Moisture index computation. works very similar to NDVI
data_dim = MI.shape
MI = np.zeros((data_dim[0],data_dim[1]))
for i in range(data_dim[0]):
	for j in range(data_dim[1]):
		MI[i,j] = ((float(B8A[i,j])-float(B11[i,j]))/(float(B8A[i,j])+float(B11[i,j]))+1)/2

iio.imwrite('NDMI-2020-01-04.png',MI)


#NDVI computation
VI_dim = B8.shape
NDVI = np.zeros((VI_dim[0],VI_dim[1]))
for i in range(VI_dim[0]):
	for j in range(VI_dim[1]):
		NDVI[i,j] = ((float(B8[i,j])-float(B4[i,j]))/(float(B8[i,j])+float(B4[i,j]))+1)/2

iio.imwrite('NDVI-2020-01-04.png',NDVI)


