import numpy as np
import matplotlib
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
from scipy.spatial import distance
from scipy import interpolate
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
from mpl_toolkits.axes_grid1 import make_axes_locatable

run = number_run()
max_distance_int_all = []
delta_angle_int_all = []

delta_angle_int_all_unsorted = []
trajectory_x_int_all_unsorted = []
trajectory_y_int_all_unsorted = []
	
	

if 'arena' in run:
	
	

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

	if os.path.exists('../../data/'+run+'/statistics/statistics.npy') == True:
		statistics = np.load('../../data/'+run+'/statistics/statistics.npy')
	else:
		statistics = np.zeros([1,12])
		
	
	for idx in range(len(files)):
		plt.close('all')
		
		recording = 'csv_records_' + files[idx]
		path = '../../data/'+run+'/rawdata/'+recording+'/'
		#print "loading trajectory"
		trajectory = np.loadtxt(skipper(path + 'robot_position.csv'), delimiter=",", usecols = (0,1,2,3))
		
		delta_angle = []
		max_distance = []
		for i in range(len(trajectory[:,3])-1):
			delta_angle.append(math.atan2(math.sin(trajectory[i+1,3] - trajectory[i,3]), math.sin(trajectory[i,3] - trajectory[i+1,3])))
			max_distance.append(float(max(abs(trajectory[i,0]),abs(trajectory[i,1]))))
			
		
		threshold_turn = 0.0
		delta_angle_thresh = np.zeros(len(delta_angle))
		delta_angle_old = 0
		for i in np.arange(1,len(delta_angle)-1,1):
			if delta_angle[i] > delta_angle[i-1] and delta_angle[i] > delta_angle[i+1]:
				delta_angle_thresh[i] = 1

			
				

		
	
		binsize = 50
		threshold = 0.6 # upper percentage to be plotted, turning threshold
		
		delta_angle_int = []
		max_distance_int = []
		trajectory_x_int = []
		trajectory_y_int = []
		
		for y in range(0, len(delta_angle)-binsize, binsize):
			delta_angle_int.append(sum(delta_angle[y:y+binsize]))
			
		for y in range(0, len(trajectory[:,0])-binsize-1, binsize):
			trajectory_x_int.append(sum(trajectory[y:y+binsize,0]))
			trajectory_y_int.append(sum(trajectory[y:y+binsize,1]))
		
		for y in range(0, len(max_distance)-binsize, binsize):
			max_distance_int.append(sum(max_distance[y:y+binsize]))
			
			
		delta_angle_int = [i/binsize * 50 for i in delta_angle_int]
		max_distance_int = [i/binsize for i in max_distance_int]
		
		trajectory_x_int = [trajectory_x_int[i]/binsize for i in range(len(trajectory_x_int)) if delta_angle_int[i] > max(delta_angle_int)-((max(delta_angle_int)-min(delta_angle_int))*threshold)]
		trajectory_y_int = [trajectory_y_int[i]/binsize for i in range(len(trajectory_y_int)) if delta_angle_int[i] > max(delta_angle_int)-((max(delta_angle_int)-min(delta_angle_int))*threshold)]
		delta_angle_int = [delta_angle_int[i] for i in range(len(delta_angle_int)) if delta_angle_int[i] > max(delta_angle_int)-((max(delta_angle_int)-min(delta_angle_int))*threshold)]
		
		delta_angle_int_all_unsorted.append(delta_angle_int)
		trajectory_x_int_all_unsorted.append(trajectory_x_int)
		trajectory_y_int_all_unsorted.append(trajectory_y_int)
		
		
		mat = [trajectory_x_int,trajectory_y_int, delta_angle_int ]
		mat = np.array(mat).T
		
		
		heatmap_resolution = 16
		heatmap_xy = np.zeros([heatmap_resolution, heatmap_resolution])
		heatmap_data = np.zeros([heatmap_resolution, heatmap_resolution])

		maximum = minimum = 3.0
		step = 2*3.0/heatmap_resolution
		idx = -1
		idx2 = -1

		amount_data_threshold = 5	

		for i in np.arange(- minimum, maximum, step):
			idx = idx + 1
			for  y in np.arange(- minimum, maximum, step):
				idx2 = (idx2+1)%heatmap_resolution
				for z in range(len(mat[:,0])):
					if mat[z,0] > i-step/2 and mat[z,0] < i+step/2 and mat[z,1] > y-step/2 and mat[z,1] < y+step/2 and heatmap_xy[idx][idx2] < amount_data_threshold:
						heatmap_xy[idx][idx2] = float(heatmap_xy[idx][idx2] + 1.0)
						heatmap_data[idx][idx2] = float(heatmap_data[idx][idx2] + mat[z,2])
						
				#print heatmap_data / heatmap_xy
		for sublist in range(len(heatmap_xy)):
			for x in range(len(heatmap_xy[sublist])):
				if heatmap_xy[sublist][x] < amount_data_threshold:
					heatmap_xy[sublist][x] = 0

		#heatmap_xy = [0 for sublist in heatmap_xy for x in sublist if x < amount_data_threshold]		
				
		fig6 = plt.figure(figsize =(5,4), dpi=300)
		ax = fig6.add_subplot(111)	
		im = ax.imshow(heatmap_data/heatmap_xy, extent=[-3,3,-3,3])
		#im.set_clim([20,100])
		fig6.colorbar(im,ax=ax)
		#divider = make_axes_locatable(ax)
		#cax = divider.append_axes("right", size="5%", pad=0.05)
		#im.set_clim([40,110])
		fig6.savefig('../../data/'+run+'/plots/angle/'+recording+'heatmap_turn_over_time.jpg', dpi = 300, bbox_inches='tight')
		
		

		
		
		#x = y = np.arange(min(mat[:,0]), max(mat[:,0]), float(max(mat[:,0])-min(mat[:,0]))/10.0)
		#X,Y = np.meshgrid(x, y)
		## Interpolate (x,y,z) points [mat] over a normal (x,y) grid [X,Y]
		##   Depending on your "error", you may be able to use other methods
		#Z = interpolate.griddata((mat[:,0], mat[:,1]), mat[:,2], (X,Y), method='nearest')
		#fig0 = plt.figure(figsize =(6,6), dpi=300)
		#ax = fig0.add_subplot(111)	
		#ax.pcolormesh(X,Y,Z)

		#fig0.tight_layout()
		
		#fig0.savefig('../../data/'+run+'/plots/angle/'+recording+'turn_over_position.jpg', dpi = 300)
		
		
			
	
		
		fig1 = plt.figure(figsize =(6,4), dpi=300)
		ax = fig1.add_subplot(411)	
		ax.plot(delta_angle, '.b')
		ax2 = fig1.add_subplot(412)	
		ax2.plot(max_distance, '.r')
		ax3 = fig1.add_subplot(413)	
		ax3.plot(delta_angle_int, '.m')
		ax4 = fig1.add_subplot(414)	
		ax4.plot(max_distance_int, '.k')
		
		fig1.savefig('../../data/'+run+'/plots/angle/'+recording+'turn_over_time.jpg', dpi = 300)
		
		
		
			
		
			

			
		s = sorted(zip(max_distance_int,delta_angle_int,))
		max_distance_int, delta_angle_int = map(list, zip(*s))
		
		xvalues = np.zeros([10])
		yvalues = np.zeros([10])
		yvalues_std = np.zeros([10])
		index = 0
		for i in np.arange(min(max_distance_int)+(max(max_distance_int)-min(max_distance_int))/10 , max(max_distance_int), (max(max_distance_int)-min(max_distance_int))/10):
			xvalues[index] = i
			ystore = []
			number_values = 0
			for y in range(len(max_distance_int)):
				if max_distance_int[y] <= i:
					ystore.append(delta_angle_int[y])
			yvalues[index] = float(sum(ystore))/float(len(ystore))
			yvalues_std[index] = np.std(ystore)		
			index = index + 1
			
		delta_angle_int_all.append(yvalues)
		max_distance_int_all.append(xvalues)
			

			
		fig2 = plt.figure(figsize =(4,4), dpi=300)
		ax = fig2.add_subplot(111)	
		ax.plot(xvalues, yvalues, '.b')
		fig2.savefig('../../data/'+run+'/plots/angle/'+recording+'turn_over_distance.jpg', dpi = 300)
		
		
		
		

		
		
max_distance_flat = [x for sublist in max_distance_int_all for x in sublist]
delta_angle_flat = [x for sublist in delta_angle_int_all for x in sublist]
max_distance_flat = [max_distance_flat[i] for i in range(len(max_distance_flat)) if delta_angle_flat[i] != 0]
delta_angle_flat = [delta_angle_flat[i] for i in range(len(delta_angle_flat)) if delta_angle_flat[i] != 0]
polynomial = np.poly1d(np.polyfit(max_distance_flat, delta_angle_flat, 3))
x_polynomial = np.arange(np.amin(max_distance_flat), np.amax(max_distance_flat) , 0.01)

#fig4 = plt.figure(figsize =(6,6), dpi=200)
#ax = fig4.add_subplot(111)
#plt.rcParams.update({'font.size': 16})
#for i in range(len(max_distance_int_all)):	
	#ax.plot(max_distance_int_all[i], delta_angle_int_all[i], '.', ms= 10)
	#ax.plot(x_polynomial, polynomial(x_polynomial), '-k')
#ax.set_ylim([np.amin(np.ma.masked_equal(delta_angle_int_all,0))*0.95, np.amax(delta_angle_int_all)*1.05])
#ax.set_xlim([0, 2.5])
#ax.set_ylabel('delta angle (rad/sec)')
#ax.set_xlabel('distance center (m)')
#fig4.tight_layout()
#fig4.savefig('../../data/arena_all/plots/turns_over_distance/'+run+'turn_over_distance.jpg', dpi = 300)	

#np.save('../../data/arena_all/plots/turns_over_distance/rawdata/'+run+'turn_over_distance.npy', [max_distance_flat,delta_angle_flat])

mat = [sum(trajectory_x_int_all_unsorted, []),sum(trajectory_y_int_all_unsorted, []), sum(delta_angle_int_all_unsorted, []) ]
mat = np.array(mat).T

#print mat[:,0]

#x = y = np.arange(min(mat[:,0]), max(mat[:,0]),  (max(mat[:,0])-min(mat[:,0]))/20.0)
#X,Y = np.meshgrid(x, y)
## Interpolate (x,y,z) points [mat] over a normal (x,y) grid [X,Y]
##   Depending on your "error", you may be able to use other methods
##Z = interpolate.griddata((mat[:,0], mat[:,1]), mat[:,2], (X,Y), method='linear',fill_value= np.mean(mat[:,2]) )
#Z = interpolate.griddata((mat[:,0], mat[:,1]), mat[:,2], (X,Y), method='linear',fill_value= min(mat[:,2])-50)
#fig0 = plt.figure(figsize =(6,6), dpi=300)
#ax = fig0.add_subplot(111)	
#c = ax.pcolormesh(X,Y,Z)
#fig0.colorbar(c)
#ax.plot(mat[:,0], mat[:,1], '.k', ms = 1)

#fig0.tight_layout()

#fig0.savefig('../../data/'+run+'/plots/angle/turn_over_position_all.jpg', dpi = 300)


#fig5 = plt.figure(figsize =(8,8), dpi=300)
#ax = fig5.add_subplot(111, projection="3d")	
#ax.scatter3D(mat[:,0], mat[:,1], mat[:,2], c = mat[:,2])
#ax.view_init(90, 90)
#ax.w_zaxis.line.set_lw(0.)
#ax.set_zticks([])

#fig5.savefig('../../data/'+run+'/plots/angle/turn_over_position_all_scatter.jpg', dpi = 300, bbox_inches='tight')

heatmap_resolution = 16
heatmap_xy = np.zeros([heatmap_resolution, heatmap_resolution])
heatmap_data = np.zeros([heatmap_resolution, heatmap_resolution])

maximum = minimum = 3.0
step = 2*3.0/heatmap_resolution
idx = -1
idx2 = -1

#print len(mat[:,0])
#print len(mat[:,1])

amount_data_threshold = 10	

for i in np.arange(- minimum, maximum, step):
	idx = idx + 1
	for  y in np.arange(- minimum, maximum, step):
		idx2 = (idx2+1)%heatmap_resolution
		for z in range(len(mat[:,0])):
			if mat[z,0] > i-step/2 and mat[z,0] < i+step/2 and mat[z,1] > y-step/2 and mat[z,1] < y+step/2 and heatmap_xy[idx][idx2] < amount_data_threshold:
				heatmap_xy[idx][idx2] = float(heatmap_xy[idx][idx2] + 1.0)
				heatmap_data[idx][idx2] = float(heatmap_data[idx][idx2] + mat[z,2])



#print heatmap_data / heatmap_xy
for sublist in range(len(heatmap_xy)):
	for x in range(len(heatmap_xy[sublist])):
		if heatmap_xy[sublist][x] < amount_data_threshold:
			heatmap_xy[sublist][x] = 0

#heatmap_xy = [0 for sublist in heatmap_xy for x in sublist if x < amount_data_threshold]		
		
fig6 = plt.figure(figsize =(5,4), dpi=300)
ax = fig6.add_subplot(111)	
im = ax.imshow(heatmap_data/heatmap_xy, extent=[-3,3,-3,3])
#im.set_clim([20,100])
fig6.colorbar(im,ax=ax)
#divider = make_axes_locatable(ax)
#cax = divider.append_axes("right", size="5%", pad=0.05)
#im.set_clim([40,110])
fig6.savefig('../../data/arena_all/plots/turns_over_distance/'+run+'_turn_position.jpg', dpi = 300, bbox_inches='tight')
		
		
fig7 = plt.figure(figsize =(5,4), dpi=300)
ax = fig7.add_subplot(111)	
im = ax.imshow(heatmap_xy, extent=[-3,3,-3,3])
#im.set_clim([20,100])
fig7.colorbar(im,ax=ax)
fig7.savefig('../../data/arena_all/plots/turns_over_distance/'+run+'_amount_datapoints.jpg', dpi = 300, bbox_inches='tight')

	
