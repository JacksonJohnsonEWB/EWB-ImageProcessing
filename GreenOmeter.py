#Jackson Johnson
#Written for the Hartford Proffession Chapter of EWB-USA
#January 2020
#jackson.david.johnson@gmail.com

#computes the cloud cover and vegatitation coverage for a given satellite image

import numpy as np
from matplotlib.image import imread
import matplotlib.pyplot as plt
import imageio as iio


#I am using a seperate script to crop the raw images as it makes them easier to work with.
#The file names below represent the cropped versions.  
filnames = ['2018-12-30.png',
			'2019-01-04.png',
			'2019-01-09.png',
			'2019-01-14.png',
			'2019-01-19.png',
			'2019-01-24.png',
			'2019-01-29.png',
			'2019-02-03.png',
			'2019-02-08.png',
			'2019-03-10.png',
			'2019-03-30.png',
			'2019-04-04.png',
			'2019-04-14.png',
			'2019-04-24.png',
			'2019-05-04.png',
			'2019-05-09.png',
			'2019-05-14.png',
			'2019-05-19.png',
			'2019-05-24.png',
			'2019-05-29.png',
			'2019-06-03.png',
			'2019-06-08.png',
			'2019-06-13.png',
			'2019-06-23.png',
			'2019-07-13.png',
			'2019-08-02.png',
			'2019-08-12.png',
			'2019-08-22.png',
			'2019-08-27.png',
			'2019-09-01.png',
			'2019-09-11.png',
			'2019-09-26.png',
			'2019-10-01.png',
			'2019-10-11.png',
			'2019-10-21.png',
			'2019-11-10.png',
			'2019-11-20.png',
			'2019-11-25.png',
			'2019-12-05.png',
			'2019-12-10.png',
			'2019-12-20.png',
			'2019-12-30.png',
			'2020-01-14.png',
			'2020-01-19.png',
			'2020-01-24.png']




def HSL_Convert(RGBpix,SF):
	R = RGBpix[0]/SF
	G = RGBpix[1]/SF
	B = RGBpix[2]/SF
	
	Cmax = max(R,G,B)
	Cmin = min(R,G,B)
	Delta = Cmax-Cmin
	CmaxPos = np.argmax(RGBpix)

	
	#Lightness Calculation
	L = (Cmax+Cmin)/2
	
	#Saturation Calculation
	S = Delta/(1-np.absolute(2*L-1))
	
	#Hue Calculation
	if Delta == 0:
		H = 0
	else:
		if CmaxPos == 0:
			H = (G-B)/(Cmax-Cmin)*60
		if CmaxPos == 1:
			H = (2+(B-R)/(Cmax-Cmin))*60
		if CmaxPos == 2:
			H = (4+(R-G)/(Cmax-Cmin))*60
	
	return [H,S,L]



for k in filnames:
	#The text file is going to contain green coverage and cloud cover percentages
	#for the pictures in the list above. Handy for plotting in excel.
	text_Data = open('PlantActivity.txt','a')
	
	#Read in the image as array the is width x height x 3 and get it's shape
	data = imread(k)
	data_dim = data.shape
	
	#initialize the counting variables (or reset after the first loop)
	cloudCount = 0
	greenCount = 0
	brownCount = 0
	
	#Here is where we start looping through the individual pixels. I need to look 
	#at map functions. Some possiblility to speed increases. Let me know if you
	#get them to work
	for i in range(data_dim[0]):
		for j in range(data_dim[1]):
			
			#Here is where the individual pixel is converted to HSL with the above function
			HSLout = HSL_Convert(data[i,j,:],1)
			
			#These are the decision gates for determining if a pixel is cloud, green,
			#or other (dirt in my case). Feel free to tune the values in the logic 
			#statements to pick narrower or wider bands of colors. These just worked
			#for my situation
			if HSLout[2] > .8:
				cloudCount = cloudCount + 1
				data[i,j,:] = [0,0,1]
			elif 40 < HSLout[0] < 220:
				data[i,j,:] = [0,1,0]
				greenCount = greenCount + 1
			else:
				brownCount = brownCount + 1
				data[i,j,:] = [1,0,0]
	
	#Here is the math for turing the cloud and green counters into percentages. Notice
	#that the green percentage is the percentage of the image remaining after cloud 
	#cover has been removed
	cloudCover = cloudCount/(data_dim[0]*data_dim[1])*100
	PlantAvtivity = greenCount/(data_dim[0]*data_dim[1]-cloudCount)*100
	
	#write the data out to the text file
	text_Data.write(k+','+str(cloudCover)+','+str(PlantAvtivity)+'\n')
	
	# write out the mask to an image. Nice when you are tuning the logic gates above.
	iio.imwrite('GOM-Mask-'+k,data)
	del data
	del data_dim
	
	#I'm closing the text file (which saves the data) because I was expieriencing 
	#computer crashes and didn't want to loose the data. In theory, you should just
	#be able to close it outside the loop and save a little I/O time.
	text_Data.close()
