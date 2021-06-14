import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker
from scipy.optimize import curve_fit
import pylab
import pandas as pd
import sys
import os
sys.path.append("../run_modules/")
from number_run import number_run
from robot_settings import size_robot 
import matplotlib.lines as mlines

run = number_run()
robot_size = size_robot()

def func(x, a, b, c):
	return a * np.exp(-b * x) + c


print 'statistics plots'

statistics_1 = np.load('/home/neuro/Documents/spiking-insect-vision/docs/nrp_collision_avoidance/data/run_57_clutter_checkerboard/statistics/statistics_robot_size_wl_4040.npy')
statistics_2 = np.load('/home/neuro/Documents/spiking-insect-vision/docs/nrp_collision_avoidance/data/run_58_clutter_fixed_v/statistics/statistics_robot_size_wl_4040.npy')
maximum_distance_1 = np.load('/home/neuro/Documents/spiking-insect-vision/docs/nrp_collision_avoidance/data/run_57_clutter_checkerboard/statistics/maximum_distance.npy')
maximum_distance_2 = np.load('/home/neuro/Documents/spiking-insect-vision/docs/nrp_collision_avoidance/data/run_58_clutter_fixed_v/statistics/maximum_distance.npy')
#print statistics
plot_color = []
plot_color_2 = []

red_patch = mlines.Line2D([],[],  markerfacecolor='red', color='w', marker = 'o', label='collision')
blue_patch = mlines.Line2D([],[], markerfacecolor='blue',color='w',marker = 's', label='left arena')
cyan_patch = mlines.Line2D([],[],markerfacecolor='magenta',color='w',marker = '<', label='time over')
black_patch = mlines.Line2D([],[],color='k',marker = 'o', label='adaptive velocity')
grey_patch = mlines.Line2D([],[],color='grey',marker = 'v', label='fixed velocity')





		
for i in range(len(statistics_1)):
	if statistics_1[i,2] == '0.0' and maximum_distance_1[i] > 24:
		statistics_1[i,4] = statistics_1[i,3]
		plot_color.append('bs')
	elif statistics_1[i,2] == '0.0' and maximum_distance_1[i] <= 24: 
		statistics_1[i,4] = statistics_1[i,3]
		plot_color.append('m<')
	elif statistics_1[i,2] == '1.0': 
		plot_color.append('ro')

		
for i in range(len(statistics_2)):
	if statistics_2[i,4] == '0.0' and maximum_distance_2[i] > 24:
		statistics_2[i,4] = statistics_2[i,3]
		plot_color_2.append('bs')
	elif statistics_2[i,4] == '0.0' and maximum_distance_2[i] <= 24: 
		statistics_2[i,4] = statistics_2[i,3]
		plot_color_2.append('m<')
	else:
		plot_color_2.append('ro')




print len(plot_color_2)
print len(statistics_2)


	
number_bins = 12
print 'plot success and events over obstacle density'
runs_no_collision_array_1 = []
runs_no_collision_array_2 = []
for i in np.arange(0, max(statistics_1[:,1].astype(float)),max(statistics_1[:,1].astype(float))/number_bins):
	number_runs = 0
	runs_no_collision = 0
	for j in range(len(statistics_1[:,1])):
		if abs(i-float(statistics_1[j,1])) <= max(statistics_1[:,1].astype(float))/number_bins:
			number_runs = number_runs + 1
			#print number_runs
			if plot_color[j] != 'ro':
				runs_no_collision = runs_no_collision +1
				#print runs_no_collision
	if number_runs != 0:
		runs_no_collision_array_1.append(float(runs_no_collision)/float(number_runs)*100)
	else:
		runs_no_collision_array_1.append(0)
		
for i in np.arange(0, max(statistics_2[:,1].astype(float)),max(statistics_2[:,1].astype(float))/number_bins):
	number_runs = 0
	runs_no_collision = 0
	for j in range(len(statistics_2[:,1])):
		if abs(i-float(statistics_2[j,1])) <= max(statistics_2[:,1].astype(float))/number_bins:
			number_runs = number_runs + 1
			#print number_runs
			if plot_color_2[j] != 'ro':
				runs_no_collision = runs_no_collision +1
				#print runs_no_collision
	if number_runs != 0:
		runs_no_collision_array_2.append(float(runs_no_collision)/float(number_runs)*100)
	else:
		runs_no_collision_array_2.append(0)

plt.rcParams.update({'font.size': 8.0})
fig8 = plt.figure(figsize =(6,4), dpi=300)
ax2 = fig8.add_subplot(211)
for i in range(len(statistics_1)):
	ax2.plot(statistics_1[i,1], (float(statistics_1[i,3])/50.0)/60.0, plot_color[i], linestyle = 'None')
ax2.set_ylabel('time (min)')
#ax2.set_xlabel('obstacle density (%)')
ax2.legend(handles=[red_patch, blue_patch, cyan_patch], fontsize='x-small')
ax = fig8.add_subplot(212)
#ax.bar(np.arange(0, max(statistics[:,1].astype(float)),max(statistics[:,1].astype(float))/number_bins),runs_no_collision_array, max(statistics[:,1].astype(float))/number_bins -0.2, color = 'k')
ax.plot(np.arange(0, max(statistics_1[:,1].astype(float)),max(statistics_1[:,1].astype(float))/number_bins), runs_no_collision_array_1, 'o', c = 'k')
ax.plot(np.arange(0, max(statistics_2[:,1].astype(float)),max(statistics_2[:,1].astype(float))/number_bins), runs_no_collision_array_2, 'v', c = 'grey')
ax.plot(np.arange(0, max(statistics_1[:,1].astype(float)),max(statistics_1[:,1].astype(float))/number_bins), runs_no_collision_array_1, c = 'k')
ax.plot(np.arange(0, max(statistics_2[:,1].astype(float)),max(statistics_2[:,1].astype(float))/number_bins), runs_no_collision_array_2, c = 'grey')
ax.set_ylabel('success rate (%)')
ax.set_xlabel('obstacle density (%)')
ax.set_ylim([-10, 110])
ax.set_xlim([0, 40])
ax.legend(handles=[black_patch, grey_patch], loc='lower left', fontsize='x-small')
ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
ax.yaxis.set_major_locator(ticker.MultipleLocator(20))
ax.grid()
fig8.tight_layout()
  
fig8.savefig('/home/neuro/Documents/spiking-insect-vision/docs/nrp_collision_avoidance/docs/clutter_results_new.jpg', dpi = 300)

