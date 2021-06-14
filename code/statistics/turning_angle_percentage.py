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

## robot size 30 x 40 cm
## robot diagonal 50 cm
## obstacle size 40 x 40 cm
## minimum distance robot-obstacle = 45 cm

red_patch = mpatches.Patch(color='red', label='collision')
blue_patch = mpatches.Patch(color='blue', label='left arena')
cyan_patch = mpatches.Patch(color='magenta', label='time over')

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
	statistics = np.zeros([1,9])

plot_color = []

for i in range(len(statistics)):
	if statistics[i,4] == '0.0' and float(statistics[i,3]) > 50000.0:
		statistics[i,4] = float(statistics[i,3])
		plot_color.append('m.')
	elif statistics[i,4] == '0.0' and float(statistics[i,3]) <= 50000.0:
		statistics[i,4] = float(statistics[i,3])
		plot_color.append('b.')
	else:
		plot_color.append('r.')

turning_angles = np.zeros([1,2])

for idx in range(len(files)):
	
	recording = 'csv_records_' + files[idx]
	path = '../../data/'+run+'/rawdata/'+recording+'/'
	print "loading trajectory"
	trajectory = np.loadtxt(skipper(path + 'robot_position.csv'), delimiter=",", usecols = (0,3))
	turning_angle = 0.0
	runtime = int(len(trajectory))
	for i in range(runtime-1):
		if float(i) <= float(statistics[idx,4]):
			turning_angle = turning_angle + abs(np.degrees(trajectory[i+1,1])*np.pi - np.degrees(trajectory[i,1])*np.pi)

				
		else:
			break

	

	turning_angles = np.concatenate((turning_angles, [[float(turning_angle)/float(statistics[idx,4]), files[idx]]]), axis = 0)

if turning_angles[0,0] == '0.0':
	turning_angles = np.delete(turning_angles, 0, 0)
	
fig3 = plt.figure(figsize =(6,4), dpi=300)
ax = fig3.add_subplot(111)
for i in range(len(statistics)):
	ax.plot(float(statistics[i,1]), turning_angles[i][0], plot_color[i])
ax.set_ylabel('turning angle / second')
ax.set_xlabel('obstacle density (%)')
ax.legend(handles=[red_patch, blue_patch, cyan_patch], fontsize='x-small')
#ax.set_ylim([0.0034, 0.0038])

#plt.show()
fig3.tight_layout()
fig3.savefig('../../data/'+run+'/plots/final/turning_angles.jpg', dpi = 300)

fig4 = plt.figure(figsize =(6,4), dpi=300)
ax = fig4.add_subplot(111)
for i in range(len(statistics)):
	ax.plot(float(statistics[i,8]), turning_angles[i][0], plot_color[i])
ax.set_ylabel('turning angle / second')
ax.set_xlabel('velocity (%)')
ax.legend(handles=[red_patch, blue_patch, cyan_patch], fontsize='x-small')
#ax.set_ylim([0.0034, 0.0038])

#plt.show()
fig4.tight_layout()
fig4.savefig('../../data/'+run+'/plots/final/turning_angles_velocity.jpg', dpi = 300)

#print statistics
np.save('../../data/'+run+'/statistics/turn_angles.npy', [files, turning_angles[:][0],turning_angles[:][1] ])

turn_spikes = np.load('../../data/'+run+'/statistics/turn_spikes.npy')

figure = []

for i in range(len(turn_spikes)):
	for j in range(len(turning_angles)):
		if turn_spikes[i,0] == turning_angles[j,1]:
			figure.append([turning_angles[i][0], turn_spikes[i][1], turn_spikes[i][2], turn_spikes[i][3]])

print figure

y = []
x = []
for i in range(len(figure)):
	if plot_color[i] != 'm.':
		y = np.append(y,float(figure[i][0])/float(figure[i][3]))
		x = np.append(x,float(statistics[i,1]))

x_sorted = np.sort(x)
	
coef = np.polyfit(x,y,1)
poly1d_fn = np.poly1d(coef) 


gradient, intercept, r_value, p_value, std_err = stats.linregress(x,y)

black_patch = mpatches.Patch(color='black', label='fit without time over data, r2 = ' + str((r_value**2).round(2)))

fig5 = plt.figure(figsize =(6,4), dpi=300)
ax = fig5.add_subplot(111)
for i in range(len(statistics)):
	ax.plot(float(figure[i][2]), float(figure[i][0])/float(figure[i][3]), plot_color[i])
ax.plot(x_sorted, poly1d_fn(x_sorted), 'k')
ax.set_ylabel('angle / turn (' + u'\N{DEGREE SIGN}' + ' / turn)')
ax.set_xlabel('obstacle density (%)')
ax.legend(handles=[red_patch, blue_patch, cyan_patch, black_patch], fontsize='x-small')
#ax.set_ylim([0.0034, 0.0038])

#plt.show()
fig5.tight_layout()
fig5.savefig('../../data/'+run+'/plots/final/turn_strength.jpg', dpi = 300)

y = []
x = []
for i in range(len(figure)):
	if plot_color[i] != 'm.':
		y = np.append(y,float(figure[i][1]))
		x = np.append(x,float(figure[i][0]))


x_sorted = np.sort(x)
	
coef = np.polyfit(x,y,1)
poly1d_fn = np.poly1d(coef) 


gradient, intercept, r_value, p_value, std_err = stats.linregress(x,y)


black_patch = mpatches.Patch(color='black', label='fit without time over data, r2 = ' + str((r_value**2).round(2)))

fig6 = plt.figure(figsize =(6,4), dpi=300)
ax = fig6.add_subplot(111)
for i in range(len(statistics)):
	ax.plot( float(figure[i][0]),float(figure[i][1]), plot_color[i])
ax.plot(x_sorted, poly1d_fn(x_sorted), 'k')
ax.set_ylabel('angle ('+ u'\N{DEGREE SIGN}' +')')
ax.set_xlabel('spikes')
ax.legend(handles=[red_patch, blue_patch, cyan_patch, black_patch], fontsize='x-small')
#ax.set_ylim([0.08, 0.4])

#plt.show()
fig6.tight_layout()
fig6.savefig('../../data/'+run+'/plots/final/turn_strength_over_spikes.jpg', dpi = 300)

fig7 = plt.figure(figsize =(6,4), dpi=300)
ax = fig7.add_subplot(111)
for i in range(len(statistics)):
	ax.plot(float(statistics[i,8]), float(figure[i][0])/float(figure[i][3]), plot_color[i])
ax.set_ylabel('angle / turn')
ax.legend(handles=[red_patch, blue_patch, cyan_patch], fontsize='x-small')
ax.set_xlabel('velocity')
#ax.set_ylim([0.0034, 0.0038])

#plt.show()
fig7.tight_layout()
fig7.savefig('../../data/'+run+'/plots/final/turn_strength_velocity.jpg', dpi = 300)


	
	
		
	
