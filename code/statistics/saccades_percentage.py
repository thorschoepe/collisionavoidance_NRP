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
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.patches as mpatches
import sys
sys.path.append("../run_modules/")
from number_run import number_run
from robot_settings import size_robot 

run = number_run()
robot_size = size_robot() # in meters

# Construct the columns for the different powers of x
def get_r2_statsmodels(x, y, k=1):
    xpoly = np.column_stack([x**i for i in range(k+1)])    
    return sm.OLS(y, xpoly).fit().rsquared


statistics = np.load('../../data/'+run+'/statistics/statistics_robot_size_wl_'+str(int(robot_size[0]*100))+str(int(robot_size[1]*100))+'.npy')

red_patch = mpatches.Patch(color='red', label='collision')
blue_patch = mpatches.Patch(color='blue', label='left arena')
magenta_patch_2 = mpatches.Patch(color='magenta', label='time over')
magenta_patch = mpatches.Patch(color='magenta', label='no extreme turns')
cyan_patch = mpatches.Patch(color='cyan', label='all turns')

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
            
#print statistics[:,4]

for i in range(len(files)):
 files[i] = re.sub('\.npy$', '', files[i])

files.sort(key = lambda date: datetime.strptime(date, '%Y-%m-%d_%H_%M'))

saccades_percentage = np.zeros([1,5])

for idx in range(len(files)):
	
	oszillator_before_crash = []
	extreme_oszillator_before_crash = []
	turns = 0
	extreme_turns = 0
	
	recording = 'csv_records_' + files[idx]
	path = '../../data/'+run+'/rawdata/'+recording+'/'
	print "loading oszillator spikes"
	oszillator_1 = np.loadtxt(skipper(path + 'oszillator_1_spikes.csv'), delimiter=",", usecols = (0,1))
	oszillator_2 = np.loadtxt(skipper(path + 'oszillator_2_spikes.csv'), delimiter=",", usecols = (0,1))
	oszillator = np.concatenate((oszillator_1, oszillator_2), axis = 0)
	
	print min(oszillator_1[:,0])
	
	for i in range(len(oszillator)):
		
		if float(oszillator[i,1]) <= float(statistics[idx,4])*20.0:
			oszillator_before_crash = 	np.concatenate((oszillator_before_crash, [oszillator[i,0]]), axis = 0)
			if oszillator[i,0] == 4129 or oszillator[i,0] == 4225:
				turns = turns + 1
			elif oszillator[i,0] == 4034 or oszillator[i,0] == 4180:
				extreme_oszillator_before_crash = 	np.concatenate((extreme_oszillator_before_crash, [oszillator[i,0]]), axis = 0)
				extreme_turns = extreme_turns + 1
		else:
			print oszillator[i,1]
			print statistics[idx,4]
			break
			
	saccades_percentage = np.concatenate((saccades_percentage,[[files[idx],float(len(oszillator_before_crash))/float(statistics[idx,4]), float(turns)/float(statistics[idx,4]),float(len(extreme_oszillator_before_crash))/float(statistics[idx,4]), float(extreme_turns)/float(statistics[idx,4])]]), axis = 0)
	#print saccades_percentage

figure = []
for i in range(len(saccades_percentage)):
	for j in range(len(statistics)):
		if saccades_percentage[i,0] == statistics[j,0]:
			figure.append([statistics[j,0], saccades_percentage[i,1],statistics[j,1], saccades_percentage[i,2], saccades_percentage[i,3], saccades_percentage[i,4],  plot_color[j], plot_color2[j]])

#print figure

fig3 = plt.figure(figsize =(6,4), dpi=300)
ax = fig3.add_subplot(111)
for i in range(len(statistics)):
	ax.plot(figure[i][2], float(figure[i][1])*50, figure[i][6])
ax.set_ylabel('# turning spikes/s')
ax.set_xlabel('obstacle density (%)')
ax.legend(handles=[red_patch, blue_patch, magenta_patch_2], fontsize='x-small')
#ax.set_ylim([0.0034, 0.0038])

#plt.show()
fig3.tight_layout()
fig3.savefig('../../data/'+run+'/plots/saccades_spikes.jpg', dpi = 300)

fig4 = plt.figure(figsize =(6,4), dpi=300)
ax = fig4.add_subplot(111)
for i in range(len(statistics)):
	ax.plot(figure[i][2], float(figure[i][3])*50, figure[i][6])
ax.set_ylabel(' # turns/s')
ax.set_xlabel('obstacle density (%)')
ax.legend(handles=[red_patch, blue_patch, magenta_patch_2], fontsize='x-small')
#ax.set_ylim([0.008, 0.022])

#plt.show()
fig4.tight_layout()
fig4.savefig('../../data/'+run+'/plots/turns_number.jpg', dpi = 300)

y = []
x = []
y2 = []
for i in range(len(statistics)):
	y = np.append(y, (float(figure[i][1])-float(figure[i][4])*96.0)/(float(figure[i][3])-float(figure[i][4])))
	y2 = np.append(y2, (float(figure[i][1]))/float(figure[i][3]))
	x = np.append(x, float(figure[i][2]))
		
coef = np.polyfit(x,y,1)
poly1d_fn = np.poly1d(coef) 

coef2 = np.polyfit(x,y2,2)
poly1d_fn2 = np.poly1d(coef2) 

r2 = get_r2_statsmodels(x, y2, 2)

x_sorted = np.sort(x)

gradient, intercept, r_value, p_value, std_err = stats.linregress(x,y)

gradient2, intercept2, r_value2, p_value2, std_err2 = stats.linregress(x,y2)

fig5 = plt.figure(figsize =(6,4), dpi=300)
ax = fig5.add_subplot(111)
for i in range(len(statistics)):
	#if figure[i][3] != '0.0':
		ax.plot(figure[i][2], (float(figure[i][1])-float(figure[i][4])*96.0)/(float(figure[i][3])-float(figure[i][4])), 'm.')
		ax.plot(figure[i][2], (float(figure[i][1]))/float(figure[i][3]), 'c+')
		
magenta_patch = mpatches.Patch(color='magenta', label='no extreme turns, r2 = ' + str((r_value**2).round(2)))
cyan_patch = mpatches.Patch(color='cyan', label='all turns, r2 = '  + str(r2.round(2)))

		
ax.plot(x, poly1d_fn(x), 'm')
ax.plot(x_sorted, poly1d_fn2(x_sorted), 'c')
ax.set_ylabel(' # spikes / turn')
ax.set_xlabel('obstacle density (%)')
ax.set_ylim([-5, 30])
ax.legend(handles=[cyan_patch, magenta_patch], fontsize='x-small')

#plt.show()
fig5.tight_layout()
fig5.savefig('../../data/'+run+'/plots/saccades_per_turn_no_extreme.jpg', dpi = 300)

fig6 = plt.figure(figsize =(6,4), dpi=300)
ax = fig6.add_subplot(111)
for i in range(len(statistics)):
	if figure[i][3] != '0.0':
		ax.plot(float(figure[i][1])/float(figure[i][3]), float(statistics[i,8])*30.0, figure[i][6])
		#ax.plot(float(figure[i][3]), float(statistics[i,8])*30.0, figure[i][4])
ax.set_xlabel(' # spikes / turn')
ax.legend(handles=[red_patch, blue_patch, magenta_patch_2], fontsize='x-small')
ax.set_ylabel(' velocity (m/s)')
#ax.set_xlim([0, 30])

#plt.show()
fig6.tight_layout()
fig6.savefig('../../data/'+run+'/plots/velocity_over_spikes_per_saccade.jpg', dpi = 300)

#print statistics
np.save('../../data/'+run+'/statistics/turn_spikes.npy', figure)

fig7 = plt.figure(figsize =(6,4), dpi=300)
ax = fig7.add_subplot(111)
for i in range(len(statistics)):
	ax.plot(float(figure[i][3])*30.0, float(statistics[i,8])*30, figure[i][6])
ax.set_xlabel(' # turns/s')
ax.set_ylabel('velocity (m/s)')
ax.legend(handles=[red_patch, blue_patch, magenta_patch_2], fontsize='x-small')
#ax.set_ylim([0.008, 0.022])

#plt.show()
fig7.tight_layout()
fig7.savefig('../../data/'+run+'/plots/turns_number_velocity.jpg', dpi = 300)






#print figure


fig4 = plt.figure(figsize =(6,4), dpi=300)
ax = fig4.add_subplot(111)
for i in range(len(statistics)):
	ax.plot(figure[i][2], float(figure[i][4])*30.0, figure[i][6])
ax.set_ylabel(' # extreme turns/s')
ax.set_xlabel('obstacle density (%)')
ax.legend(handles=[red_patch, blue_patch, magenta_patch_2], fontsize='x-small')
#ax.set_ylim([0.008, 0.022])

#plt.show()
fig4.tight_layout()
fig4.savefig('../../data/'+run+'/plots/extreme_turns_number.jpg', dpi = 300)


