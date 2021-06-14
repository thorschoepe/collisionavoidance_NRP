import sys
import numpy as np
import matplotlib.pyplot as plt
import itertools
import os
import re
from datetime import datetime
import math
import matplotlib.patches as mpatches
import matplotlib.patches as patches
sys.path.append("../run_modules/")
from number_run import number_run
from robot_settings import size_robot 

robot_size = size_robot()

sys.path.append("../../data/arena_all/statistics/")
from arena_data import data

Data, plots = data()

distance_wall = np.load("../../data/arena_all/statistics/distance_wall.npy")

red_patch = mpatches.Patch(color='red', label='collision')

walls = []

walls.append(patches.Rectangle((-3,-3.1),0.2,6.2, zorder = 2))
walls.append(patches.Rectangle((-3,-3.1),6,0.2, zorder = 2))
walls.append(patches.Rectangle((-3,2.9),6,0.2, zorder = 2))
walls.append(patches.Rectangle((3,-3),0.2,1.1, zorder = 2))
walls.append(patches.Rectangle((3,1.9),0.2,1.1, zorder = 2))
walls.append(patches.Rectangle((3,-2.1),4,0.2, zorder = 2))
walls.append(patches.Rectangle((3,1.9),4,0.2, zorder = 2))
walls.append(patches.Rectangle((7,-2),0.2,0.6, zorder = 2))
walls.append(patches.Rectangle((7,1.4),0.2,0.6, zorder = 2))
walls.append(patches.Rectangle((7,-1.6),4,0.2, zorder = 2))
walls.append(patches.Rectangle((7,1.4),4,0.2, zorder = 2))
walls.append(patches.Rectangle((11,-1.6),0.2,0.7, zorder = 2))
walls.append(patches.Rectangle((11,0.9),0.2,0.5, zorder = 2))
walls.append(patches.Rectangle((11,-1.1),4,0.2, zorder = 2))
walls.append(patches.Rectangle((11,0.9),4,0.2, zorder = 2))
walls.append(patches.Rectangle((15,-1),4,0.2, zorder = 2))
walls.append(patches.Rectangle((15,0.8),4,0.2, zorder = 2))
walls.append(patches.Rectangle((19,-0.9),4,0.2, zorder = 2))
walls.append(patches.Rectangle((19,0.7),4,0.2, zorder = 2))
walls.append(patches.Rectangle((23,-0.8),4,0.2, zorder = 2))
walls.append(patches.Rectangle((23,0.6),4,0.2, zorder = 2))
walls.append(patches.Rectangle((27,-0.7),4,0.2, zorder = 2))
walls.append(patches.Rectangle((27,0.5),4,0.2, zorder = 2))
walls.append(patches.Rectangle((31,-0.6),4,0.2, zorder = 2))
walls.append(patches.Rectangle((31,0.4),4,0.2, zorder = 2))
walls.append(patches.Rectangle((35,-0.5),4,0.2, zorder = 2))
walls.append(patches.Rectangle((35,0.3),4,0.2, zorder = 2))
walls.append(patches.Rectangle((39,-0.4),4,0.2, zorder = 2))
walls.append(patches.Rectangle((39,0.2),4,0.2, zorder = 2))

def plot_traject(plots, plot, Data, data_xlabel):
	robot_size = 0.4
	patch = []
	patch2 = 0
	plt.close('all')
	
	fig3 = plt.figure(figsize =(4,4), dpi=300)
	ax3 = fig3.add_subplot(111)
	colours = ['k', 'maroon', 'orange', 'magenta']
	
	
	for experiment in range(len(plots[plot][1])):	# go through different experiments
		
		for i in range(len(Data.run)):
			if plots[plot][1][experiment] == Data.run[i]:
				patch_label = plots[plot][0][i]	
		
		if 'corridor' not in plots[plot][1][experiment]:
			if isinstance(patch_label, float):
				patch.append(mpatches.Patch(color=colours[experiment], label=str(float(patch_label/robot_size))))
			else:
				patch.append(mpatches.Patch(color=colours[experiment], label=patch_label))
				
		else:
			patch.append(mpatches.Patch(color=colours[experiment], label=str(float(patch_label))))
		if isinstance(patch_label, float):
			patch2 = [mpatches.Patch(color=colours[experiment], label=str(float(patch_label/robot_size)))]
		else:
			patch2 = [mpatches.Patch(color=colours[experiment], label=patch_label)]
		
		print experiment
		
		
		
		path_files = '../../data/'+plots[plot][1][experiment]+'/world_objects_coordinates/final/'
		
		
		
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
		
		trajectories = []
		
		for idx in range(len(files)):
			
		
			recording = 'csv_records_' + files[idx]
			
			oszillator1 = np.loadtxt(skipper('../../data/'+plots[plot][1][experiment]+'/rawdata/' + recording+ '/oszillator_1_spikes.csv'), delimiter=",", usecols = (0,1))

			path = '../../data/'+plots[plot][1][experiment]+'/rawdata/'+recording+'/'
			#print "loading trajectory"
			trajectory = np.loadtxt(skipper(path + 'robot_position.csv'), delimiter=",", usecols = (0,1,2,3))
			objects = np.load('../../data/'+plots[plot][1][experiment]+'/world_objects_coordinates/final/'+files[idx]+'.npy')
			
			trajectory_new = []
			trajectory_new_2 = []
			
			for idx in range(len(trajectory[:,0])):
					trajectory_new = np.append(trajectory_new,trajectory[idx,1]/0.4)
					trajectory_new_2 = np.append(trajectory_new_2,trajectory[idx,0]/0.4)
					if -trajectory[idx,0] > 35:
						break
			trajectories = np.append(trajectories, trajectory_new)

			#check if robot left arena
			runtime = int(len(trajectory[:,0]))
			
			if 'corridor' not in plots[plot][1][experiment] and 'tunnel' not in plots[plot][1][experiment] :
				for i in range(len(trajectory[:,0])):
					if abs(trajectory[i,0]) > 15 or abs(trajectory[i,1]) > 15:
						if runtime == int(len(trajectory[:,0])):
							runtime = i - 1
			elif 'corridor' in plots[plot][1][experiment]:
				for i in range(len(oszillator1[:,1])):
					if np.multiply(oszillator1[i,1], 0.001) > 100 and  oszillator1[i,0] == 4034:
						runtime = int(oszillator1[i,1]/20)
						print runtime
						break
						


			# calculate robot edge positions in global world
			robot_edge_positions_x = [[] for _ in range(runtime)]
			robot_edge_positions_y = [[] for _ in range(runtime)]
			robot_edge_positions = [[] for _ in range(runtime)]

			for i in range(runtime):
				for b in np.arange(-0.10, 0.15, 0.05):	# changed a to b
					for a in np.arange(-0.10, 0.15, 0.05):	# changed b to a
						robot_edge_positions_x[i].append(math.cos(1.5708-trajectory[i,3])*a+math.sin(1.5708-trajectory[i,3])*b+trajectory[i,0])
						robot_edge_positions_y[i].append(math.sin(1.5708-trajectory[i,3])*a-math.cos(1.5708-trajectory[i,3])*b+trajectory[i,1])
			
											

			
			if 'arena' in plots[plot][1][experiment]:
				ax3.plot(np.array(robot_edge_positions_x)/0.4,np.array(robot_edge_positions_y)/0.4, color = colours[experiment], ms= 0.1, alpha = 0.1)
				ax3.set_xlim([-10,10])
				ax3.set_ylim([-10,10])
			elif 'corridor' in plots[plot][1][experiment]:
				ax3.plot(np.array(robot_edge_positions_x)*-1,robot_edge_positions_y, color = colours[experiment], ms= 0.1, alpha = 0.5)
				fig3.set_figheight(4)
				fig3.set_figwidth(10)
				ax3.set_xlim([-3.5,44])
				ax3.set_ylim([-3.5,3.5])
				for i in range(len(walls)):
					ax3.add_patch(walls[i])
			elif 'tunnel' in plots[plot][1][experiment]:
				ax3.plot(-trajectory_new_2,trajectory_new, color = colours[experiment], lw= 5, alpha = 0.7)
				fig3.set_figheight(5)
				fig3.set_figwidth(7)
				ax3.set_xlim([0,25/0.4])
				ax3.set_ylim([-0.4/0.4,0.4/0.4])
				ax3.set_xlabel('position (a.u.)')
				ax3.set_ylabel('position (a.u.)')
				
				plt.rc('font', size=20)  
				plt.rc('axes', labelsize=20)    # fontsize of the x and y labels
				plt.rc('xtick', labelsize=20)    # fontsize of the tick labels
				plt.rc('ytick', labelsize=20)    # fontsize of the tick labels
				plt.rc('legend', fontsize=20) 
				
				fig4 = plt.figure(figsize =(4,4), dpi=300)
				ax4 = fig4.add_subplot(111)
				ax4.hist(np.divide(trajectories, patch_label/2.0), bins = 60, range = (-1,1), color = colours[experiment], normed = True)
				ax4.legend(handles=patch2, fontsize='x-small')
				ax4.set_xlim([-1,1])
				ax4.set_ylim([0,8])
				ax4.set_yticks(range(0,10,2))
				fig4.tight_layout()
				fig4.savefig('../../data/arena_all/plots/distance_wall/y_distribution' + str(plot) + str(experiment) + '.jpg', dpi = 300)


				
			elif 'gap' in plots[plot][1][experiment]:
				ax3.plot(trajectory[:,0],trajectory[:,1], color = colours[experiment], lw= 5, alpha = 0.5)
				fig3.set_figheight(4)
				fig3.set_figwidth(10)
				ax3.set_xlim([-5,5])
				ax3.set_ylim([-5,5])
				fig3.tight_layout()
				
			#ax3.set_title(data_xlabel)
			fig3.tight_layout()
			ax3.legend(handles=patch, fontsize='x-small')
			fig3.savefig('../../data/arena_all/plots/distance_wall/plot_traj' + str(plot) + '.jpg', dpi = 300)
			


			



for plot in range(len(plots)):
	runs = 'none'
	data_x = []
	data_y = []
	data_xlabel = []
	for experiment in range(len(plots[plot][1])):
		for i in range(len(Data.run)):
			for distance in range(len(distance_wall)):
				if 'arena' in Data.run[i] and  plots[plot][1][experiment] == Data.run[i] and distance_wall[distance][0] == Data.run[i]:
					data_x.append(plots[plot][0][i])
					data_y.append(distance_wall[distance][1])
					data_xlabel = plots[plot][2]
					runs = Data.run[i]
				elif plots[plot][1][experiment] == Data.run[i]:
					data_xlabel = plots[plot][2]
					runs = Data.run[i]
					
	
	#if 'arena' in runs:
		#lists = sorted(itertools.izip(*[data_x, data_y]))
		#data_x, data_y = list(itertools.izip(*lists))
		#fig1 = plt.figure(figsize =(6,6), dpi=300)
		#ax1 = fig1.add_subplot(111)
		#ax1.plot(data_x, data_y, 'b')
		#ax1.plot(data_x, data_y, '.k', ms = 8)
		#ax1.set_xlabel(data_xlabel)
		#ax1.set_ylabel('mean wall clearance')
		#ax1.set_ylim([1,2.2])
		#ax1.set_xlim([min(data_x)-((max(data_x)-min(data_x))/10.0), max(data_x)+((max(data_x)-min(data_x))/10.0)])
		#fig1.savefig('../../data/arena_all/plots/distance_wall/plot_' + str(plot) + '.jpg', dpi = 300)
	
	plot_traject(plots, plot, Data, data_xlabel)
	


