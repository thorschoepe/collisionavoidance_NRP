import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as patches
import matplotlib.cm as cm
import os
import re
from datetime import datetime
import sys
sys.path.append("../run_modules/")
from number_run import number_run
import matplotlib.ticker as ticker
from robot_settings import size_robot 

robot_size = size_robot()
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
        if 'random_environment.jpg' in file:
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
            
statistics = np.load('../../data/'+run+'/statistics/statistics_robot_size_wl_'+str(int(robot_size[0]*100))+str(int(robot_size[1]*100))+'.npy')


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
		
if os.path.exists('../../data/'+run+'/statistics/spikes_wta_mean.npy') == True:
	spikes_wta_mean = np.load('../../data/'+run+'/statistics/spikes_wta_mean.npy')
else:
	spikes_wta_mean = []
	
if os.path.exists('../../data/'+run+'/statistics/spikes_wta_std.npy') == True:
	spikes_wta_std = np.load('../../data/'+run+'/statistics/spikes_wta_std.npy')
else:
	spikes_wta_std = []
		
               
            
for idx in range(len(files)):
	#if 'csv_records_' + files[idx] + 'random_environment' not in files_plots:
		
		plt.close('all')
		
		#print files[idx]

		recording = 'csv_records_' + files[idx]
		path = '../../data/'+run+'/rawdata/'+recording+'/'


		#print "loading trajectory"
		#trajectory = np.loadtxt(skipper(path + 'robot_position.csv'), delimiter=",", usecols = (0,1))

		#objects = np.load('../../data/'+run+'/world_objects_coordinates/final/'+files[idx]+'.npy')

		
		#print "done"
		



		##print trajectory



		#rect = []


		#for i in range(len(objects)):
			#rect.append(patches.Rectangle((objects[i][0]-0.2,objects[i][1]-0.2),0.4,0.4, zorder = 2))

		#fig = plt.figure(figsize =(4,4), dpi=300)
		#ax = fig.add_subplot(111)
		#if float(statistics[idx,2]) == 1.0:
			#ax.plot(trajectory[statistics[idx,4].astype(float),0],trajectory[statistics[idx,4].astype(float),1],"*r", ms = 8)
		#for i in range(len(rect)):
			#ax.add_patch(rect[i])
		#for i in np.arange(statistics[idx,4].astype(float)):
			#ax.plot(trajectory[i,0],trajectory[i,1], '.',c = cm.rainbow(np.divide(float(i),float(len(trajectory[:,0])))), zorder = 1)

				
				
		#ax.set_xlim([-15,15])
		#ax.set_ylim([-15,15])
		#ax.grid()



		#fig.savefig('../../data/'+run+'/plots/trajectories/'+recording+'random_environment.jpg', dpi = 300)
		
		#plt.close('all')
		
		print "loading integrator spikes"
		integrator_rl = np.loadtxt(skipper(path + 'integrator_rl_spikes.csv'), delimiter=",", usecols = (0,1))
		integrator_lr = np.loadtxt(skipper(path + 'integrator_lr_spikes.csv'), delimiter=",", usecols = (0,1))
		print "loading wta spikes"
		wta = np.loadtxt(skipper(path + 'wta_spikes.csv'), delimiter=",", usecols = (0,1))
		print "loading oszillator spikes"
		oszillator1 = np.loadtxt(skipper(path + 'oszillator_1_spikes.csv'), delimiter=",", usecols = (0,1))
		oszillator2 = np.loadtxt(skipper(path + 'oszillator_2_spikes.csv'), delimiter=",", usecols = (0,1))
		print 'min and max motor 1:'
		print (min(oszillator1[:,0]))
		print (max(oszillator1[:,0]))
		print 'min and max motor 2:'
		print (min(oszillator2[:,0]))
		print (max(oszillator2[:,0]))
		
		xlimit = max(np.concatenate((integrator_rl[:,1], integrator_lr[:,1], wta[:,1], oszillator1[:,1], oszillator2[:,1])))
		
		fig2 = plt.figure(figsize =(10,5), dpi=300)
		ax = fig2.add_subplot(611)
		ax.plot(np.multiply(integrator_rl[:,1],0.001),integrator_rl[:,0], '. r',  ms = 0.1)
		ax.plot(np.multiply(integrator_lr[:,1], 0.001),integrator_lr[:,0]-64, '. b' , ms = 0.1)
		ax.set_xlim([0,np.multiply(statistics[idx,4].astype(float), 0.02)])
		ax.set_ylabel('integrators')
		ax.set_yticks([])
		ax.set_xticks([])

		ax4 = fig2.add_subplot(613)
		ax4.plot(np.multiply(wta[:,1], 0.001),wta[:,0], '.r', ms = 0.8)
		ax4.hlines(np.mean(wta[:,0]),0,np.multiply(statistics[idx,4].astype(float), 0.02), colors='k', linewidth=1)
		ax4.hlines(np.mean(wta[:,0]) + np.std(wta[:,0]),0,np.multiply(statistics[idx,4].astype(float), 0.02), colors='k', linewidth=0.3)
		ax4.hlines(np.mean(wta[:,0]) - np.std(wta[:,0]),0,np.multiply(statistics[idx,4].astype(float), 0.02), colors='k', linewidth=0.3)
		ax4.set_xlim([0,np.multiply(statistics[idx,4].astype(float), 0.02)])
		ax4.set_ylabel('wta')
		ax4.set_yticks([])
		ax4.set_xticks([])

		ax2 = fig2.add_subplot(615)
		ax2.plot(np.multiply(oszillator1[:,1], 0.001),oszillator1[:,0], '. g', ms = 0.4)
		ax2.set_xlim([0,np.multiply(statistics[idx,4].astype(float), 0.02)])
		ax2.set_ylabel('right turn')
		ax2.set_yticks([])
		ax2.set_xticks([])

		ax3 = fig2.add_subplot(616)
		ax3.plot(np.multiply(oszillator2[:,1], 0.001),oszillator2[:,0], '. k', ms = 0.4)
		ax3.set_xlim([0,np.multiply(statistics[idx,4].astype(float), 0.02)])
		ax3.set_ylabel('left turn')
		ax3.set_xlabel('time (s)')
		ax3.set_yticks([])
		
		ax5 = fig2.add_subplot(612)
		spikes = []
		spikes = np.append(spikes, integrator_lr[:,1])
		spikes = np.append(spikes, integrator_rl[:,1])
		#print spikes
		ax5.hist(np.multiply(spikes, 0.001), bins = np.arange(0, np.multiply(statistics[idx,4].astype(float), 0.02), 1))
		ax5.set_xlim([0,np.multiply(statistics[idx,4].astype(float), 0.02)])
		y_vals = ax5.get_yticks()
		ax5.set_yticklabels(['{:3.0f}'.format(x / 128) for x in y_vals])
		ax5.yaxis.set_ticks(np.arange(0, 18000, 6000))
		ax5.set_xticks([])
		
		ax6 = fig2.add_subplot(614)
		spikes = []
		spikes = np.append(spikes, wta[:,1])
		ax6.hist(np.multiply(spikes, 0.001), bins = np.arange(0, np.multiply(statistics[idx,4].astype(float), 0.02), 1))
		ax6.set_xlim([0,np.multiply(statistics[idx,4].astype(float), 0.02)])
		ax6.yaxis.set_ticks(np.arange(0, 4, 2))
		ax6.set_xticks([])




		fig2.savefig('../../data/'+run+'/plots/spikes/'+recording+'_spikes.jpg', dpi = 300)
		
		plt.close('all')
		
		spikes_wta_mean = np.concatenate((spikes_wta_mean, [np.mean(wta[:,0]), files[idx]]), axis = 0)
		spikes_wta_std = np.concatenate((spikes_wta_std, [np.std(wta[:,0]), files[idx]]), axis = 0)
		
		print spikes_wta_std
		np.save('../../data/'+run+'/statistics/spikes_wta_mean.npy', spikes_wta_mean)	
		np.save('../../data/'+run+'/statistics/spikes_wta_std.npy', spikes_wta_std)	

		

