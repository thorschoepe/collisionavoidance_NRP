import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as patches
import matplotlib.cm as cm
import os
import re
import sys
from datetime import datetime
sys.path.append("../run_modules/")
from number_run import number_run

run = number_run()

print '2dplots_clearance_calclaution'

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
print files

# load file names of saved plots

path_plots = '../../data/'+run+'/plots/clearance_calculation/'

files_plots = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path_plots):
    for file in f:
        if 'random_environment_clearance.jpg' in file:
            files_plots.append(file)
            
for i in range(len(files_plots)):
 files_plots[i] = re.sub('\.jpg$', '', files_plots[i])


def skipper(fname):
    with open(fname) as fin:
        no_comments = (line for line in fin if not line.lstrip().startswith('#'))
        next(no_comments, None) # skip header
        for row in no_comments:
            yield row
            
for idx in range(len(files)):
	if 'csv_records_' + files[idx] + 'random_environment_clearance' not in files_plots:

		recording = 'csv_records_' + files[idx]
		path = '../../data/'+run+'/rawdata/'+recording+'/'


		print "loading objects"

		objects = np.load('../../data/'+run+'/world_objects_coordinates/final/'+files[idx]+'.npy')

		print "done"
		#print len(DataAll1D[:,0])






		rect = []

		#for i in range(len(rectangles_x)):
			#rect.append(patches.Rectangle((rectangles_x[i],rectangles_y[i]),0.4,0.4))
		for i in range(len(objects)):
			rect.append(patches.Rectangle((objects[i][0]-0.5,objects[i][1]-0.5),1,1, zorder = 2, lw=0))

		fig = plt.figure(figsize =(4,4), dpi=300)
		plt.axis('off')
		ax = fig.add_subplot(111)
		for i in range(len(rect)):
			ax.add_patch(rect[i])
		ax.set_xlim([-25,25])
		ax.set_ylim([-25,25])
		plt.gca().set_axis_off()
		plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
				hspace = 0, wspace = 0)
		plt.margins(0,0)
		#ax.grid()
		

		#plt.show()

		fig.savefig('../../data/'+run+'/plots/clearance_calculation/'+recording+'random_environment_clearance.jpg', dpi = 300)

		#xlimit = max(np.concatenate((integrator_rl[:,1], integrator_lr[:,1], wta[:,1], oszillator1[:,1], oszillator2[:,1])))
		#
		#fig2 = plt.figure(figsize =(10,5), dpi=300)
		#ax = fig2.add_subplot(411)
		#ax.plot(integrator_rl[i,1],integrator_rl[i,0], '. b',  ms = 0.1)
		#ax.plot(integrator_lr[:,1],integrator_lr[:,0]-64, '. b' , ms = 0.1)
		#ax.set_xlim([0,xlimit])

		#ax4 = fig2.add_subplot(412)
		#for i in range(len(wta[:,1])):
			#ax4.plot(wta[i,1],wta[i,0], '.', c = cm.rainbow(np.divide(wta[i,1],xlimit)), ms = 0.8)
		#ax4.set_xlim([0,xlimit])

		#ax2 = fig2.add_subplot(413)
		#ax2.plot(oszillator1 [:,1],oszillator1 [:,0], '. g', ms = 0.4)
		#ax2.set_xlim([0,xlimit])

		#ax3 = fig2.add_subplot(414)
		#ax3.plot(oszillator2 [:,1],oszillator2 [:,0], '. k', ms = 0.4)
		#ax3.set_xlim([0,xlimit])

		##plt.show()

		#fig2.savefig('/home/neuro/Documents/spiking-insect-vision/docs/nrp_collision_avoidance/data/plots/'+recording+'_cluttered1_spikes.jpg', dpi = 300)

