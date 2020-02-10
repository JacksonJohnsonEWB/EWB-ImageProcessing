
from osgeo import gdal
import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib as mpl
import math

gdal.UseExceptions()

file = 's06_e036_1arc_v3.tif'

ds = gdal.Open(file)

data = ds.ReadAsArray()*3.281
tenthdata = data[800-50:800+50,1786-60:1786+40]

width = 100
height = 100
Stepsize = .1

xgrad = np.zeros([height,width])
ygrad = np.zeros([height,width])

for i in range(height-2):
	for j in range(width-2):
		xgrad[i+1][j+1] = tenthdata[i+1][j+2]-tenthdata[i+1][j]
		ygrad[i+1][j+1] = tenthdata[i+2][j+1]-tenthdata[i][j+1]



def calcNewPosition(currentPosition,xgrad,ygrad,stepsize):
        #Calculate the new position given a current location, step size and gradient field

        #Find bounding box around current point
        xmin = int(math.floor(currentPosition[0]))
        xmax = int(math.ceil(currentPosition[0]))

        ymin = int(math.floor(currentPosition[1]))
        ymax = int(math.ceil(currentPosition[1]))


        
        xremain = currentPosition[0]%xmin
        yremain = currentPosition[1]%ymin


        
        ##Calculate interpolated X gradient
        #Interpolate in X direction first
        xgradYmin = (xgrad[ymin][xmax]-xgrad[ymin][xmin])*xremain+xgrad[ymin][xmin]
        xgradYmax = (xgrad[ymax][xmax]-xgrad[ymax][xmin])*xremain+xgrad[ymax][xmin]


        
        #interpolate between Ymin and Ymax along calculated x values
        xgradInterp = (xgradYmax-xgradYmin)*yremain+xgradYmin

        ##Calculate Interpolated Y gradient
        #Interpolate in X direction first
        ygradYmin = (ygrad[ymin][xmax]-ygrad[ymin][xmin])*xremain+ygrad[ymin][xmin]
        ygradYmax = (ygrad[ymax][xmax]-ygrad[ymax][xmin])*xremain+ygrad[ymax][xmin]

        #interpolate between Ymin and Ymax along calculated x values
        ygradInterp = (xgradYmax-xgradYmin)*yremain+ygradYmin

        #Normalize total gradient vector
        gradMag = (xgradInterp**2+ygradInterp**2)**.5
        xgradNorm = xgradInterp/gradMag
        ygradNorm = ygradInterp/gradMag


        
        #Calculate New Postion
        xNew = stepsize*-xgradNorm+currentPosition[0]
        yNew = stepsize*-ygradNorm+currentPosition[1]

        return [xNew,yNew]


Steps = 200       

paths = 67
xstart = np.linspace(1.5,20.5,num=paths)
ystart = np.linspace(45.5,75.5,num=paths)

Position = np.zeros((Steps,2))
pathOutput = np.zeros((paths**2,Steps,2))

color = np.linspace(0,1,num=Steps)
Position[0] = [90.057,30.143]

l=0
for k in range(paths):
        for j in range(paths):
                Position[0] = [xstart[k],ystart[j]]
                for i in range(Steps-1):
                        Position[i+1] = calcNewPosition(Position[i],xgrad,ygrad,.1)
                        if not 1 < Position[i+1][0] < 98 or not 2 < Position[i+1][1] < 99:
                                Position[i+1] = Position[i]
                pathOutput[l] = Position
                l = l+1

mpl.rcParams['figure.figsize'] = 60,60
mpl.rcParams['figure.dpi'] = 100
mpl.rcParams['lines.linewidth'] = .5

plt.figure()
plt.contour(tenthdata,np.arange(4900,5700,50),colors='k')
for i in range(paths**2):
      plt.plot(pathOutput[i,:,0],pathOutput[i,:,1],'k')#,c=color,edgecolor='none')
#plt.show()

#plt.clabel(tplt,inline=1,font=50)
plt.axis('off')
plt.savefig('StreamlineOut.png',bbox_inches='tight')
