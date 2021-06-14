
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
from scipy.spatial import distance
import sys
sys.path.append("../run_modules/")
from number_run import number_run
from robot_settings import size_robot 

maximum_obstacle_density = 40
step_size = 5
robot_size = size_robot()

obstacle_density_all = []
maximum_distance_all = []
maximum_distance_xy_all = []
plot_color = []
plot_color2 = []


distances_sorted = [[] for _ in range(maximum_obstacle_density/step_size)]


run = number_run()

print 'maximum distance'


path_files = '../../data/'+run+'/world_objects_coordinates/final/'

if os.path.exists('../../data/'+run+'/statistics/maximum_distance.npy') == True:
	maximum_distance_xy_all = np.load('../../data/'+run+'/statistics/maximum_distance.npy')
else:
	maximum_distance_xy_all = np.array([])
	
print maximum_distance_xy_all

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path_files):
    for file in f:
        if '.npy' in file:
            files.append(file)
            
def skipper(fname):
    with open(fname) as fin:
        no_comments = (line for line in fin if not line.lstrip().startswith('#'))
        next(no_comments, None) # skip header
        for row in no_comments:
            yield row
            


for i in range(len(files)):
 files[i] = re.sub('\.npy$', '', files[i])

files.sort(key = lambda date: datetime.strptime(date, '%Y-%m-%d_%H_%M'))

if os.path.exists('../../data/'+run+'/statistics/statistics_robot_size_wl_'+str(int(robot_size[0]*100))+str(int(robot_size[1]*100))+'.npy') == True:
	statistics = np.load('../../data/'+run+'/statistics/statistics_robot_size_wl_'+str(int(robot_size[0]*100))+str(int(robot_size[1]*100))+'.npy')
else:
	statistics = np.zeros([1,12])
	
#for i in range(len(statistics)):
	#if statistics[i,4] == '0.0' and float(statistics[i,3]) > 30000.0:
		#statistics[i,4] = statistics[i,3]
		#plot_color.append('m.')
		#plot_color2.append("m")
	#elif statistics[i,4] == '0.0' and float(statistics[i,3]) <= 30000.0:
		#statistics[i,4] = statistics[i,3]
		#plot_color.append('b.')
		#plot_color2.append("b")
	#else:
		#plot_color.append('r.')
		#plot_color2.append("r")
		


	

# calculate percentage obstacle coverage 
for idx in range(len(maximum_distance_xy_all), len(files), 1):
		plt.close('all')
		
		print files[idx]
		print str(idx + 1) + ' of ' + str(len(files))
		image = img.imread('../../data/'+run+'/plots/clearance_calculation/csv_records_'+files[idx]+'random_environment_clearance.jpg')
		pixels_image = 0
		obstacles_percentage = 0
		
		for line in image:
			for pixel in line:
				temp_r, temp_g, temp_b = pixel
				pixels_image = pixels_image + 1
				if temp_r == 255 and temp_g == 255 and temp_b == 255:
					obstacles_percentage = obstacles_percentage + 1
		
		obstacles_percentage = 100 - (float(obstacles_percentage)/float(pixels_image))*100
		


		recording = 'csv_records_' + files[idx]
		path = '../../data/'+run+'/rawdata/'+recording+'/'
		#print "loading trajectory"
		trajectory = np.loadtxt(skipper(path + 'robot_position.csv'), delimiter=",", usecols = (0,1,2,3))
		
		distances_euclid = []
		for i in range(len(trajectory[:,0])):
			distances_euclid.append(abs(distance.euclidean([0,0],[trajectory[i,0], trajectory[i,1]])))
		
		obstacle_density_all.append(obstacles_percentage)
		maximum_distance_all.append(max(distances_euclid))
		maximum_distance_xy_all = np.append(maximum_distance_xy_all, max(max(abs(trajectory[:,0])), max(abs(trajectory[:,1]))))
		
		print maximum_distance_xy_all

		if statistics[idx,2] == '1.0': 
			plot_color.append('ro')
		elif statistics[idx,2] == '0.0' and maximum_distance_xy_all[idx] > 24.0:
			plot_color.append('bs')
		elif statistics[idx,2] == '0.0' and maximum_distance_xy_all[idx] <= 24.0: 
			plot_color.append('m<')

		

		for i in np.arange(0,maximum_obstacle_density,step_size):
			for y in range(len(maximum_distance_all)):
				if obstacle_density_all[y]> i and obstacle_density_all[y]< i+step_size:
					distances_sorted[int(i/step_size)].append(maximum_distance_all[y]/0.4) # normalizing to au
			
		distances_sorted_mean = [np.mean(distances_sorted[i]) for i in range(len(distances_sorted))]
		distances_sorted_std = [np.std(distances_sorted[i]) for i in range(len(distances_sorted))]
		distances_sorted_std_neg = [distances_sorted_mean[i]-distances_sorted_std[i] for i in range(len(distances_sorted))]
		distances_sorted_std_pos = [distances_sorted_mean[i]+distances_sorted_std[i] for i in range(len(distances_sorted))]
		
		#for i in range(len(maximum_distance_all)):
			#if maximum_distance_all[i] < 14 and plot_color[i] == 'b.':
				#plot_color[i] = 'm.'
		
		fig = plt.figure(figsize =(6,4), dpi=300)
		ax = fig.add_subplot(111)
		print len(obstacle_density_all)
		print len(plot_color)
		for i in range(len(maximum_distance_all)):
			ax.plot(obstacle_density_all[i], maximum_distance_all[i]/0.4, plot_color[i])
		ax.plot(np.arange(0+step_size/2,maximum_obstacle_density+step_size/2,step_size), distances_sorted_mean, 'k')
		ax.plot(np.arange(0+step_size/2,maximum_obstacle_density+step_size/2,step_size), distances_sorted_mean, '.k')
		plt.fill_between(np.arange(0+step_size/2,maximum_obstacle_density+step_size/2,step_size),distances_sorted_std_neg,distances_sorted_std_pos,alpha=.1)
		ax.set_xlim([0,40])
		ax.set_ylabel('maximum distance (a.u.)')
		ax.set_xlabel('obstacle density (%)')
		fig.tight_layout()
		fig.savefig('../../data/'+run+'/plots/final/maximum_distance.jpg', dpi = 300)
		
		np.save('../../data/'+run+'/statistics/maximum_distance.npy',maximum_distance_xy_all)








