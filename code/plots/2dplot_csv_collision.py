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
print '2d plots'

# load all file names of obstacle arrays

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

path_plots = '../../data/'+run+'/plots/trajectories/'

files_plots = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path_plots):
    for file in f:
        if 'collision_csv_records_' in file:
            files_plots.append(file)
            
for i in range(len(files_plots)):
 files_plots[i] = re.sub('\.jpg$', '', files_plots[i])


# load csv without header

def skipper(fname):
    with open(fname) as fin:
        no_comments = (line for line in fin if not line.lstrip().startswith('#'))
        next(no_comments, None) # skip header
        for row in no_comments:
            yield row
            
statistics = np.load('../../data/'+run+'/statistics/statistics.npy')

plot_color = []
plot_color2 = []

for i in range(len(statistics)):
	if statistics[i,4] == '0.0' and float(statistics[i,3]) > 50000.0:
		statistics[i,4] = statistics[i,3]
		plot_color.append('m.')
		plot_color2.append('m.')
	elif statistics[i,4] == '0.0' and float(statistics[i,3]) <= 50000.0:
		statistics[i,4] = statistics[i,3]
		plot_color.append('b.')
		plot_color2.append('m.')
	else:
		plot_color.append('r.')
		plot_color2.append('c.')
		
		
               
            
for idx in range(len(files)):
	print statistics[idx,2]
	if 'collision_csv_records_' + files[idx] + '_spikes' not in files_plots and float(statistics[idx,2]) == 1.0:
		
		plt.close('all')
		
		print files[idx]

		recording = 'csv_records_' + files[idx]
		path = '../../data/'+run+'/rawdata/'+recording+'/'


		print "loading integrator spikes"
		integrator_rl = np.loadtxt(skipper(path + 'integrator_rl_spikes.csv'), delimiter=",", usecols = (0,1))
		integrator_lr = np.loadtxt(skipper(path + 'integrator_lr_spikes.csv'), delimiter=",", usecols = (0,1))
		print "loading wta spikes"
		wta = np.loadtxt(skipper(path + 'wta_spikes.csv'), delimiter=",", usecols = (0,1))
		print "loading oszillator spikes"
		oszillator1 = np.loadtxt(skipper(path + 'oszillator_1_spikes.csv'), delimiter=",", usecols = (0,1))
		oszillator2 = np.loadtxt(skipper(path + 'oszillator_2_spikes.csv'), delimiter=",", usecols = (0,1))
		print "done"
		#print len(DataAll1D[:,0])
		
		print statistics[idx,4]

		
		xlimit = max(np.concatenate((integrator_rl[:,1], integrator_lr[:,1], wta[:,1], oszillator1[:,1], oszillator2[:,1])))
		
		fig2 = plt.figure(figsize =(10,5), dpi=300)
		ax = fig2.add_subplot(411)
		ax.plot(np.multiply(integrator_rl[:,1],0.001),integrator_rl[:,0], '. r',  ms = 0.1)
		ax.plot(np.multiply(integrator_lr[:,1], 0.001),integrator_lr[:,0]-64, '. b' , ms = 0.1)
		ax.set_xlim([np.multiply(statistics[idx,4].astype(float),0.02)-10,np.multiply(statistics[idx,4].astype(float),0.02)+10])
		ax.set_ylabel('integrators')
		ax.set_yticks([])
		ax.set_xticks([])

		ax4 = fig2.add_subplot(412)
		ax4.plot(np.multiply(wta[:,1], 0.001),wta[:,0], '.r', ms = 0.8)
		ax4.set_xlim([np.multiply(statistics[idx,4].astype(float),0.02)-10,np.multiply(statistics[idx,4].astype(float),0.02)+10])
		ax4.set_ylabel('wta')
		ax4.set_yticks([])
		ax4.set_xticks([])

		ax2 = fig2.add_subplot(413)
		ax2.plot(np.multiply(oszillator1[:,1], 0.001),oszillator1[:,0], '. g', ms = 0.4)
		ax2.set_xlim([np.multiply(statistics[idx,4].astype(float),0.02)-10,np.multiply(statistics[idx,4].astype(float),0.02)+10])
		ax2.set_ylabel('right turn')
		ax2.set_yticks([])
		ax2.set_xticks([])

		ax3 = fig2.add_subplot(414)
		ax3.plot(np.multiply(oszillator2[:,1], 0.001),oszillator2[:,0], '. k', ms = 0.4)
		ax3.set_xlim([np.multiply(statistics[idx,4].astype(float),0.02)-10,np.multiply(statistics[idx,4].astype(float),0.02)+10])
		ax3.set_ylabel('left turn')
		ax3.set_xlabel('time (s)')
		ax3.set_yticks([])

		#plt.show()


		fig2.savefig('../../data/'+run+'/plots/spikes_collision/collision_'+recording+'_spikes.jpg', dpi = 300)
		
		plt.close('all')
		


		

