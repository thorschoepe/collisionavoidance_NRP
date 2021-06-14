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

run = number_run()
print 'obstacle density'
## obstacle size 40 x 40 cm



## load files ##############################################################################################################################
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
            
## check for collisions ####################################################################################################            
def check_collision(image, robot_2, rect_2, run, recording, trajectory):
	time_to_crash = 0.0
	collision = 0
	#image = img.imread('../../data/'+run+'/plots/trajectories/'+recording+'random_environment.jpg')
	for line in image:
		for pixel in line:
			temp_r, temp_g, temp_b = pixel
			if  140 > temp_r > 100 and 140 > temp_b > 100:
				collision = 1
				time_to_crash = calc_collision_time(robot_2, rect_2, run, recording, trajectory, time_to_crash)
				return time_to_crash, collision
	return time_to_crash, collision

### calculate the collision time #########################################################################################################            
def calc_collision_time(robot, rect, run, recording, trajectory, time_to_crash):
	print 'found collision'
	step_size = 100
	plt.close('all')
	fig2 = plt.figure(figsize =(1,1), dpi=300)
	ax2 = fig2.add_subplot(111)
	for i in range(len(rect)):
		ax2.add_patch(rect[i])
	
	# plot robot's trajectory with fixed step size and check if collision occurred by searching for overlap
	print "find collision time with stepsize: " 
	print str(step_size)
	for i in range(0, len(robot), step_size):
		ax2.add_patch(robot[i])
		coordinates = robot[i].get_xy()
		ax2.set_xlim([coordinates[0]-1,coordinates[0]+1])
		ax2.set_ylim([coordinates[1]-1,coordinates[1]+1])
		plt.gca().set_axis_off()
		plt.margins(0,0)
		#fig2.savefig('../../data/'+run+'/plots/collisions/'+recording+'random_environment_'+str(i)+'.jpg', dpi = 300)
		fig2.canvas.draw()
		image = np.frombuffer(fig2.canvas.tostring_rgb(), dtype=np.uint8)
		image = image.reshape(fig2.canvas.get_width_height()[::-1] + (3,))
		for line in image:
			for pixel in line:
				temp_r, temp_g, temp_b = pixel
				if  140 > temp_r > 100 and 140 > temp_b > 100:
					time_to_crash = i
					print 'found collision time'
					return time_to_crash
		# if no collision was found it might happen at the very end at timestep len(robot)-1, so check there
		ax2.add_patch(robot[len(robot)-1])
		coordinates = robot[len(robot)-1].get_xy()
		ax2.set_xlim([coordinates[0]-1,coordinates[0]+1])
		ax2.set_ylim([coordinates[1]-1,coordinates[1]+1])
		plt.gca().set_axis_off()
		plt.margins(0,0)
		#fig2.savefig('../../data/'+run+'/plots/collisions/'+recording+'random_environment_'+str(i)+'.jpg', dpi = 300)
		fig2.canvas.draw()
		image = np.frombuffer(fig2.canvas.tostring_rgb(), dtype=np.uint8)
		image = image.reshape(fig2.canvas.get_width_height()[::-1] + (3,))
		for line in image:
			for pixel in line:
				temp_r, temp_g, temp_b = pixel
				if  140 > temp_r > 100 and 140 > temp_b > 100:
					time_to_crash = i
					print 'found collision time'
					return time_to_crash
	# if collision still not found step might be too big so that robot collision not seen, try with quarter step size
	print str(int(step_size/4))
	for i in range(0, len(robot), int(step_size/4)):
		ax2.add_patch(robot[i])
		coordinates = robot[i].get_xy()
		ax2.set_xlim([coordinates[0]-1,coordinates[0]+1])
		ax2.set_ylim([coordinates[1]-1,coordinates[1]+1])
		plt.gca().set_axis_off()
		plt.margins(0,0)
		#fig2.savefig('../../data/'+run+'/plots/collisions/'+recording+'random_environment_'+str(i)+'.jpg', dpi = 300)
		fig2.canvas.draw()
		image = np.frombuffer(fig2.canvas.tostring_rgb(), dtype=np.uint8)
		image = image.reshape(fig2.canvas.get_width_height()[::-1] + (3,))
		for line in image:
			for pixel in line:
				temp_r, temp_g, temp_b = pixel
				if  140 > temp_r > 100 and 140 > temp_b > 100:
					time_to_crash = i
					print 'found collision time'
					return time_to_crash
		# if collision still not found step might be too big so that robot collision not seen, try with step size of one
	print str(int(step_size/10))
	for i in range(0, len(robot), int(step_size/10)):
		ax2.add_patch(robot[i])
		coordinates = robot[i].get_xy()
		ax2.set_xlim([coordinates[0]-1,coordinates[0]+1])
		ax2.set_ylim([coordinates[1]-1,coordinates[1]+1])
		plt.gca().set_axis_off()
		plt.margins(0,0)
		#fig2.savefig('../../data/'+run+'/plots/collisions/'+recording+'random_environment_'+str(i)+'.jpg', dpi = 300)
		fig2.canvas.draw()
		image = np.frombuffer(fig2.canvas.tostring_rgb(), dtype=np.uint8)
		image = image.reshape(fig2.canvas.get_width_height()[::-1] + (3,))
		for line in image:
			for pixel in line:
				temp_r, temp_g, temp_b = pixel
				if  140 > temp_r > 100 and 140 > temp_b > 100:
					time_to_crash = i
					print 'found collision time'
					return time_to_crash
	
	print 'no collision found, try to improve collision finding algorithm'




for i in range(len(files)):
 files[i] = re.sub('\.npy$', '', files[i])
files.sort(key = lambda date: datetime.strptime(date, '%Y-%m-%d_%H_%M'))
if os.path.exists('../../data/'+run+'/statistics/statistics_robot_size_wl_'+str(int(robot_size[0]*100))+str(int(robot_size[1]*100))+'.npy') == True:
	statistics = np.load('../../data/'+run+'/statistics/statistics_robot_size_wl_'+str(int(robot_size[0]*100))+str(int(robot_size[1]*100))+'.npy')
	print 'found statistics file'
else:
	statistics = np.zeros([1,12])
	

if 'arena' in run or 'cube' in run:
	fig2 = plt.figure(figsize =(4,4), dpi=300)
	ax2 = fig2.add_subplot(111)
	fig3 = plt.figure(figsize =(4,4), dpi=300)
	ax3 = fig3.add_subplot(111)
	


# calculate percentage obstacle coverage 
for idx in range(len(files)):
	if files[idx] not in statistics[:,0]:
		plt.close('all')
		
		print files[idx]
		print str(idx + 1) + ' of ' + str(len(files))
		image = img.imread('../../data/'+run+'/plots/clearance_calculation/csv_records_'+files[idx]+'random_environment_clearance.jpg')

		obstacles_percentage = 0
		pixels_image = 0
		collision = 0
		time_to_crash = 0.0
		distance_to_crash = 0
		
		for line in image:
			for pixel in line:
				temp_r, temp_g, temp_b = pixel
				pixels_image = pixels_image + 1
				if temp_r == 255 and temp_g == 255 and temp_b == 255:
					obstacles_percentage = obstacles_percentage + 1
		
		obstacles_percentage = 100 - (float(obstacles_percentage)/float(pixels_image))*100
		
		
	# calculate collision


		recording = 'csv_records_' + files[idx]
		path = '../../data/'+run+'/rawdata/'+recording+'/'
		#print "loading trajectory"
		trajectory = np.loadtxt(skipper(path + 'robot_position.csv'), delimiter=",", usecols = (0,1,2,3))
		
		#check if robot left arena
		runtime = int(len(trajectory[:,0]))
		if 'corridor' not in run and 'tunnel' not in run:
			for i in range(len(trajectory[:,0])):
				if abs(trajectory[i,0]) > 25 or abs(trajectory[i,1]) > 25:
					print 'tunnel not in run'
					if runtime == int(len(trajectory[:,0])):
						runtime = i - 1
		elif 'tunnel' in run:
			for i in range(len(trajectory[:,0])):
				if abs(trajectory[i,0]) > 50 or abs(trajectory[i,1]) > 50:
					if runtime == int(len(trajectory[:,0])):
						runtime = i - 1
						break
					
		trajectory_length_to_crash = 0.0
		colours = [ 'orange', 'm', 'mediumblue', 'orchid', 'g', 'c', 'b', 'r', 'darkseagreen','deepskyblue','olivedrab', 'coral','brown']
		# create robot rectangle for plotting
		robot = []
		robot_2 = []
		robot_coloured = []
		for i in range(runtime):
			if 'clutter' in run:
				robot.append(patches.Rectangle((trajectory[i,0]-robot_size[0]/2.0,trajectory[i,1]-robot_size[1]/2.0),robot_size[0],robot_size[1], zorder = 1, lw=0, angle=np.degrees(trajectory[i,3]), color = 'r', alpha = 0.5))
				robot_2.append(patches.Rectangle((trajectory[i,0]-robot_size[0]/2.0,trajectory[i,1]-robot_size[1]/2.0),robot_size[0],robot_size[1], zorder = 1, lw=0, angle=np.degrees(trajectory[i,3]), color = 'r', alpha = 1))
			trajectory_length_to_crash = trajectory_length_to_crash + cdist([[trajectory[i,0],trajectory[i,1]]],[[trajectory[i-1,0],trajectory[i-1,1]]],'euclidean')
			if 'arena' in run or 'cube' in run:
				robot_2.append(patches.Rectangle((trajectory[i,0]-robot_size[0]/2.0,trajectory[i,1]-robot_size[1]/2.0),robot_size[0],robot_size[1], zorder = 1, lw=0, angle=np.degrees(trajectory[i,3]), color = 'r', alpha = 0.5))
				robot.append(patches.Rectangle((trajectory[i,0]-robot_size[0]/2.0,trajectory[i,1]-robot_size[1]/2.0),robot_size[0],robot_size[1], zorder = 1, lw=0, angle=np.degrees(trajectory[i,3]), color = 'r', alpha = 0.5))
				robot_coloured.append(patches.Rectangle((trajectory[i,0]-robot_size[0]/2.0,trajectory[i,1]-robot_size[1]/2.0),robot_size[0],robot_size[1], zorder = 1, lw=0, angle=np.degrees(trajectory[i,3]), color = colours[idx]))
			if 'tunnel' in run or 'corridor' in run:
				robot.append(patches.Rectangle((-trajectory[i,0]-robot_size[0]/2.0,-trajectory[i,1]-robot_size[1]/2.0),robot_size[0],robot_size[1], zorder = 1, lw=0, angle=np.degrees(trajectory[i,3]), color = 'r', alpha = 0.5))

					
		
		
		
		
		# figure which shows all arena trjactories together ##########################################################################################
		if 'arena' in run or 'cube' in run:
			for i in range(len(robot)):
				ax2.add_patch(robot_coloured[i])
			ax2.set_xlim([-3,3])
			ax2.set_ylim([-3,3])
			ax2.grid(b=True)
			fig2.savefig('../../data/'+run+'/plots/trajectories/'+run+'overview.jpg', dpi = 300)
			
		# figure for distance estimation to edges in arena ###########################################################################################
			plt.axis('off')
			for i in range(len(robot)):
				ax3.add_patch(robot[i])
			ax3.set_xlim([-3,3])
			ax3.set_ylim([-3,3])
			plt.gca().set_axis_off()
			plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
					hspace = 0, wspace = 0)
			plt.margins(0,0)
			fig3.savefig('../../data/'+run+'/plots/trajectories/'+run+'_black_white.jpg', dpi = 300)

		
		
		
		rect = []
		rect_2 = []
		walls = []
		walls_gap = []
		
		
		obstacle_size = [1.0, 1.0]
		# array with clutter obstacles ###############################################################################################################
		objects = np.load('../../data/'+run+'/world_objects_coordinates/final/'+files[idx]+'.npy')
		for i in range(len(objects)):
			rect.append(patches.Rectangle((objects[i][0]-obstacle_size[0]/2.0,objects[i][1]-obstacle_size[0]/2.0),obstacle_size[0],obstacle_size[1], zorder = 2, lw=0, color = 'b', alpha = 0.5))
			rect_2.append(patches.Rectangle((objects[i][0]-obstacle_size[0]/2.0,objects[i][1]-obstacle_size[0]/2.0),obstacle_size[0],obstacle_size[1], zorder = 2, lw=0, color = 'b', alpha = 0.5))
		# array with corridor obstacles ###############################################################################################################
		#walls.append(patches.Rectangle((3,-3.1),0.2,6.2, zorder = 2))
		#walls.append(patches.Rectangle((-3,-3.1),6,0.2, zorder = 2))
		#walls.append(patches.Rectangle((-3,2.9),6,0.2, zorder = 2))
		#walls.append(patches.Rectangle((-3,-3),0.2,1.1, zorder = 2))
		#walls.append(patches.Rectangle((-3,1.9),0.2,1.1, zorder = 2))
		#walls.append(patches.Rectangle((-7,-2.1),4,0.2, zorder = 2))
		#walls.append(patches.Rectangle((-7,1.9),4,0.2, zorder = 2))
		#walls.append(patches.Rectangle((-7,-2),0.2,0.6, zorder = 2))
		#walls.append(patches.Rectangle((-7,1.4),0.2,0.6, zorder = 2))
		#walls.append(patches.Rectangle((-11,-1.6),4,0.2, zorder = 2))
		#walls.append(patches.Rectangle((-11,1.4),4,0.2, zorder = 2))
		#walls.append(patches.Rectangle((-11,-1.6),0.2,0.7, zorder = 2))
		#walls.append(patches.Rectangle((-11,0.9),0.2,0.5, zorder = 2))
		#walls.append(patches.Rectangle((-15,-1.1),4,0.2, zorder = 2))
		#walls.append(patches.Rectangle((-15,0.9),4,0.2, zorder = 2))
		#walls.append(patches.Rectangle((-19,-1),4,0.2, zorder = 2))
		#walls.append(patches.Rectangle((-19,0.8),4,0.2, zorder = 2))
		#walls.append(patches.Rectangle((-23,-0.9),4,0.2, zorder = 2))
		#walls.append(patches.Rectangle((-23,0.7),4,0.2, zorder = 2))
		#walls.append(patches.Rectangle((-27,-0.8),4,0.2, zorder = 2))
		#walls.append(patches.Rectangle((-27,0.6),4,0.2, zorder = 2))
		#walls.append(patches.Rectangle((-31,-0.7),4,0.2, zorder = 2))
		#walls.append(patches.Rectangle((-31,0.5),4,0.2, zorder = 2))
		#walls.append(patches.Rectangle((-35,-0.6),4,0.2, zorder = 2))
		#walls.append(patches.Rectangle((-35,0.4),4,0.2, zorder = 2))
		#walls.append(patches.Rectangle((-39,-0.5),4,0.2, zorder = 2))
		#walls.append(patches.Rectangle((-39,0.3),4,0.2, zorder = 2))
		#walls.append(patches.Rectangle((-43,-0.4),4,0.2, zorder = 2))
		#walls.append(patches.Rectangle((-43,0.2),4,0.2, zorder = 2))
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
		
		walls_gap.append(patches.Rectangle((-3.1,-8),0.2,4, zorder = 2))
		walls_gap.append(patches.Rectangle((-3.1,4),0.2,4, zorder = 2))
		walls_gap.append(patches.Rectangle((-3.1,-1),0.2,2, zorder = 2))

		
		# plot trajectories #######################################################################################################################
		plt.close('all')
		
		fig1 = plt.figure(figsize =(4,4), dpi=300)
		ax1 = fig1.add_subplot(111)
		
		#print robot
		
		if 'arena' in run or 'cube' in run:
			for i in range(len(robot_2)):
				ax1.add_patch(robot_2[i])
			ax1.set_xlim([-3,3])
			ax1.set_ylim([-3,3])
		elif 'corridor' in run:
			fig1.set_figheight(4)
			fig1.set_figwidth(10)
			for i in range(len(robot)):
				ax1.add_patch(robot[i])
			ax1.set_xlim([-3.5, 44])
			ax1.set_ylim([-3.5,3.5])
			for i in range(len(walls)):
				ax1.add_patch(walls[i])
		elif 'tunnel' in run:
			fig1.set_figheight(4)
			fig1.set_figwidth(10)
			for i in range(len(robot)):
				ax1.add_patch(robot[i])
			ax1.set_xlim([0,30])
			if 'two' in run:
				ax1.set_ylim([-1,1])
			elif 'three' in run:
				ax1.set_ylim([-1.5,1.5])
			elif 'four' in run:
				ax1.set_ylim([-2,2])
			elif 'five' in run:
				ax1.set_ylim([-2.5,2.5])
			elif 'six' in run:
				ax1.set_ylim([-3.0,3.0])
			elif 'seven' in run:
				ax1.set_ylim([-3.5,3.5])
			elif '4_5' in run:
				ax1.set_ylim([-2.25,2.25])
		elif 'gap' in run:
			for i in range(len(trajectory[:,0])):
				ax1.plot(trajectory[i,0],trajectory[i,1], '.',c = cm.cool(np.divide(float(i),float(len(trajectory[:,0])))), zorder = 2)
			ax1.set_xlim([-9,3])
			ax1.set_ylim([-8,8])
			for i in range(len(walls_gap)):
				ax1.add_patch(walls_gap[i])
		elif 'clutter' in run:
			for i in range(len(robot)):
				ax1.add_patch(robot[i])
			for i in range(len(rect)):
				ax1.add_patch(rect[i])
			major_ticks = np.arange(-25, 30, 5)
			minor_ticks = np.arange(-25, 30, 1)
			ax1.set_xticks(major_ticks)
			ax1.set_xticks(minor_ticks, minor=True)
			ax1.set_yticks(major_ticks)
			ax1.set_yticks(minor_ticks, minor=True)
			ax1.grid(which='minor', alpha=0.1, zorder = 0)
			ax1.grid(which='major', alpha=0.5, zorder = 0)
			ax1.set_xlim([-25,25])
			ax1.set_ylim([-25,25])
		else:
			print 'unknown environment type, include type in folder name'
		
		if robot_size == [0.5, 0.5] or 'clutter' not in run:

			#ax1.grid(b=True, which='minor', axis='both')
			#ax1.grid(b=True)
			fig1.savefig('../../data/'+run+'/plots/trajectories/'+recording+'random_environment.jpg', dpi = 300)
		
		ax1.grid(b=False)
		plt.gca().set_axis_off()
		plt.margins(0,0)

		#plt.close('all')
		
		
		
		
		# extract pixel values from figure
		fig1.canvas.draw()
		image = np.frombuffer(fig1.canvas.tostring_rgb(), dtype=np.uint8)
		image = image.reshape(fig1.canvas.get_width_height()[::-1] + (3,))
		plt.close('all')
		
		time_to_crash = 0.0
		collision = 0
		# calculate collision timing, distance to mid point and distance travelled
		if 'clutter' in run:
			time_to_crash, collision = check_collision(image, robot_2, rect_2, run, recording, trajectory)	
			print 'time to crash:'
			print time_to_crash
			print 'collision:'
			print collision		

		distance_to_crash = math.sqrt(trajectory[time_to_crash,0]**2 + trajectory[time_to_crash,1]**2)
		#distance_to_crash = 0 # can be ignored, not relevant anymore
		if time_to_crash == 0.0: # if did nit find crash then runtime is whole time
			runtime_2 = runtime
		else:
			runtime_2 = time_to_crash # if found crash runtime is time to crash

					
		#save relevant statistical data ################################################################################################################
		time_to_crash_no_middle = 0 # can be ignored, not relevant anymore
		object_distance = []			
		for i in range(runtime_2):
			object_distance =	np.append(object_distance, cdist([[trajectory[i,0],trajectory[i,1]]],objects,'euclidean').min())
		velocity = trajectory_length_to_crash/runtime_2
		mean_object_distance = np.mean(object_distance)
		statistics = np.concatenate((statistics,[[files[idx],float(obstacles_percentage), float(collision), runtime_2 , float(time_to_crash), distance_to_crash, int(time_to_crash_no_middle), float(trajectory_length_to_crash), float(velocity),float(mean_object_distance), float(np.std(object_distance)), float(np.min(object_distance))]]), axis = 0)
		if statistics[0,0] == '0.0':
		   statistics = np.delete(statistics, 0, 0)
		np.save('../../data/'+run+'/statistics/statistics_robot_size_wl_'+str(int(robot_size[0]*100))+str(int(robot_size[1]*100))+'.npy', statistics)
				
		

		




