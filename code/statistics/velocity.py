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
from copy import copy
from robot_settings import size_robot 

robot_size = size_robot()
velocity = []
run = number_run()

## load files ##############################################################################################################################
path_files = '../../data/'+run+'/world_objects_coordinates/final/'
files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path_files):
    for file in f:
        if '.npy' in file:
            files.append(file)
            
for i in range(len(files)):
 files[i] = re.sub('\.npy$', '', files[i])
files.sort(key = lambda date: datetime.strptime(date, '%Y-%m-%d_%H_%M'))
            
def skipper(fname):
    with open(fname) as fin:
        no_comments = (line for line in fin if not line.lstrip().startswith('#'))
        next(no_comments, None) # skip header
        for row in no_comments:
            yield row
            
if os.path.exists('../../data/'+run+'/statistics/statistics_robot_size_wl_'+str(int(robot_size[0]*100))+str(int(robot_size[1]*100))+'.npy') == True:
	statistics = np.load('../../data/'+run+'/statistics/statistics_robot_size_wl_'+str(int(robot_size[0]*100))+str(int(robot_size[1]*100))+'.npy')
	print 'found statistics file'
else:
	statistics = np.zeros([1,12])
	

   
for idx in range(len(files)):
	# load trajectory #######################################################################################################################         
	recording = 'csv_records_' + files[idx]
	path = '../../data/'+run+'/rawdata/'+recording+'/'
	#print "loading trajectory"
	trajectory = np.loadtxt(skipper(path + 'robot_position.csv'), delimiter=",", usecols = (0,1,2,3))

	#check if robot left arena
	runtime = int(len(trajectory[:,0]))
	trajectory_length_to_crash = 0.0

	for i in range(runtime):
		trajectory_length_to_crash = trajectory_length_to_crash + cdist([[trajectory[i,0],trajectory[i,1]]],[[trajectory[i-1,0],trajectory[i-1,1]]],'euclidean')
		
	velocity = np.append([velocity], trajectory_length_to_crash/runtime)
	print velocity
	print idx
	
	fig3 = plt.figure(figsize =(6,4), dpi=300)
	ax = fig3.add_subplot(111)
	for i in range(len(velocity)):
		#print statistics[i][2]
			ax.plot(statistics[i,1], velocity[i]*50*2, 'ko')
			print "velocity: "
			print float(statistics[i,8])*50.0
	ax.set_ylabel('velocity (a.u./s)')
	ax.set_xlabel('obstacle density (%)')
	#ax.legend(handles=[red_patch, blue_patch, cyan_patch], fontsize='x-small')
	ax.set_xlim([0, 40])
	#ax.set_ylim([0, 0.7])
	fig3.tight_layout()

	fig3.savefig('../../data/'+run+'/plots/final/velocity.jpg', dpi = 300)
	
	plt.close('all')


np.save('../../data/'+run+'/statistics/velocity.npy', velocity)

