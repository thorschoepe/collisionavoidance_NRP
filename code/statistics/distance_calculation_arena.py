import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as patches
import matplotlib.cm as cm
import os
import re
from datetime import datetime
from matplotlib import image as img
import math
from scipy.spatial.distance import cdist
import sys
sys.path.append("../run_modules/")
from number_run import number_run
import cv2


run = number_run()

print 'distance calculation'
import cv2   
###### load image and find contours
image = cv2.imread('../../data/'+run+'/plots/trajectories/'+run+'_black_white.jpg') 
 # Grayscale 
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
# Find Canny edges 
edged = cv2.Canny(gray, 30, 200) 
cv2.waitKey(0) 

contours, hierarchy = cv2.findContours(edged,  
    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 


### transfrom array
contours_np = np.array(contours)
transpose = contours_np.T
contours_list = transpose.tolist()
distance = []




fig1 = plt.figure(figsize =(4,4), dpi=300)
ax1 = fig1.add_subplot(111)
for i in range(len(contours)):
	for y in range(len(contours[i])):
		for z in range(len(contours[i][y])):
			ax1.plot(contours[i][y][z][0],contours[i][y][z][1] , '.k')
			distance.append(min((600.0- abs(float(contours[i][y][z][0])-600.0))/200.0, (600.0- abs(float(contours[i][y][z][0])-600.0))/200.0)) 
#plt.show()



if os.path.exists('../../data/arena_all/statistics/distance_wall.npy') == True:
	distance_wall = np.load('../../data/arena_all/statistics/distance_wall.npy')
else:
	distance_wall = np.zeros([1,2])
	
distance_wall = np.concatenate((distance_wall, [[run,sum(distance)/len(distance)]]), axis = 0)

if distance_wall[0,0] == '0.0':
   distance_wall = np.delete(distance_wall, 0, 0)

np.save( '../../data/arena_all/statistics/distance_wall.npy', distance_wall)

fig1.savefig('../../data/'+run+'/plots/trajectories/contour_black_white.jpg', dpi = 300)

print distance_wall







