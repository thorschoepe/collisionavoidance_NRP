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
import matplotlib.patches as mpatches
from scipy import stats
import sys
sys.path.append("../run_modules/")
from number_run import number_run

run = number_run()

path_files = '../../data/'+run+'/world_objects_coordinates/final/'

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

statistics = np.load('../../data/'+run+'/statistics/statistics.npy')

#print statistics
plot_color = []
plot_color2 = []

red_patch = mpatches.Patch(color='red', label='collision')
blue_patch = mpatches.Patch(color='blue', label='left arena')
cyan_patch = mpatches.Patch(color='magenta', label='time over')

for i in range(len(statistics)):
	if statistics[i,4] == '0.0' and float(statistics[i,3]) > 50000.0:
		statistics[i,4] = statistics[i,3]
		plot_color.append('m.')
		plot_color2.append("m")
	elif statistics[i,4] == '0.0' and float(statistics[i,3]) <= 50000.0:
		statistics[i,4] = statistics[i,3]
		plot_color.append('b.')
		plot_color2.append("b")
	else:
		plot_color.append('r.')
		plot_color2.append("r")


turning_spikes_difference = []
angles = []
obstacle_density = []
name =  []

for idx in range(len(files)):


	
	plt.close('all')
		
		
	bin_size = 10000.0	
			
	
	recording = 'csv_records_' + files[idx]
	path = '../../data/'+run+'/rawdata/'+recording+'/'
	#print "loading trajectory"
	trajectory = np.loadtxt(skipper(path + 'robot_position.csv'), delimiter=",", usecols = (0,3))
	
	recording = 'csv_records_' + files[idx]
	path = '../../data/'+run+'/rawdata/'+recording+'/'
	#print "loading oszillator spikes"
	oszillator_1 = np.loadtxt(skipper(path + 'oszillator_1_spikes.csv'), delimiter=",", usecols = (0,1))
	oszillator_2 = np.loadtxt(skipper(path + 'oszillator_2_spikes.csv'), delimiter=",", usecols = (0,1))
	oszillator = np.concatenate((oszillator_1, oszillator_2), axis = 0)
	
	xranges = np.arange(0,max(oszillator_1[:,1]),bin_size)
	number_spikes_1 = np.zeros(len(xranges))
	
	for i in range(len(oszillator_1[:,0])):
		bins = int(float(oszillator_1[i,1])/bin_size)
		number_spikes_1[bins] = number_spikes_1[bins] + 1 
		
	xranges = np.arange(0,max(oszillator_2[:,1]),bin_size)
	number_spikes_2 = np.zeros(len(xranges))
	
	for i in range(len(oszillator_2[:,0])):
		bins = int(float(oszillator_2[i,1])/bin_size)
		number_spikes_2[bins] = number_spikes_2[bins] + 1 
		
	
	
	
	angle_trajectory = np.zeros(len(trajectory[:,1])/(bin_size/20) +1)
	
	for i in range(len(trajectory[:,1])-1):
		bins = int(i/(bin_size/20))
		angle_trajectory[bins] = angle_trajectory[bins] + np.degrees(trajectory[i,1].astype(float))* np.pi - np.degrees(trajectory[i+1,1].astype(float))* np.pi
	
		
	
		
	xaxis = np.arange(0,min(max(oszillator_1[:,1]),max(oszillator_2[:,1])), bin_size)
	xaxis_trajectory = np.arange(0,len(trajectory[:,1]), (bin_size/20))
	
	

	fig5 = plt.figure(figsize =(6,6), dpi=300)
	ax = fig5.add_subplot(311)
	ax.plot(np.multiply(range(len(trajectory[:,0])),0.02), np.degrees(trajectory[:,1].astype(float))* np.pi,'.r')
	ax.set_ylabel('angle (' + u'\N{DEGREE SIGN})')
	ax.set_xlabel('time (s)')
	ax.set_ylim([-200,200])
	ax4 = fig5.add_subplot(312)
	ax4.bar(xaxis_trajectory/50,angle_trajectory[0:len(xaxis_trajectory)],(bin_size/20)/50, ecolor = 'm')
	ax4.set_ylabel('$\Delta$ angle (' + u'\N{DEGREE SIGN})')
	ax4.set_xlabel('time (s)')
	ax5 = fig5.add_subplot(313)
	ax5.bar(xaxis/1000,number_spikes_1[0:len(xaxis)]-number_spikes_2[0:len(xaxis)],bin_size/1000, ecolor = 'm')
	ax5.set_ylabel('# spikes')
	ax5.set_xlabel('time (s)')
	ax5.set_ylim([-500,500])


	
	

	#plt.show()
	fig5.tight_layout()
	fig5.savefig('../../data/'+run+'/plots/turning_angles/turn_angle_time'+ files[idx]+'.jpg', dpi = 300)
	
	
	angles = np.append(angles, abs(angle_trajectory[0:len(xaxis)]))
	turning_spikes_difference = np.append(turning_spikes_difference, abs(number_spikes_1[0:len(xaxis)]-number_spikes_2[0:len(xaxis)]))
	obstacle_density = np.append(obstacle_density, [statistics[idx,1]]*len(abs(angle_trajectory[0:len(xaxis)])))

np.save('../../data/'+run+'/statistics/obstacle_density.npy', obstacle_density)	
np.save('../../data/'+run+'/statistics/angles.npy', angles)
np.save('../../data/'+run+'/statistics/turning_spikes_difference.npy', turning_spikes_difference)



	

	


	
