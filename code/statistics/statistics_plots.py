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

run = number_run()
robot_size = size_robot()

def func(x, a, b, c):
	return a * np.exp(-b * x) + c


print 'statistics plots'

statistics = np.load('../../data/'+run+'/statistics/statistics_robot_size_wl_'+str(int(robot_size[0]*100))+str(int(robot_size[1]*100))+'.npy')
maximum_distance = np.load('../../data/'+run+'/statistics/maximum_distance.npy')

#print statistics
plot_color = []
plot_color2 = []

red_patch = mpatches.Patch(color='red', label='collision')
blue_patch = mpatches.Patch(color='blue', label='left arena')
cyan_patch = mpatches.Patch(color='magenta', label='time over')

		
for i in range(len(statistics)):
	if statistics[i,4] == '0.0' and maximum_distance[i] > 24:
		statistics[i,4] = statistics[i,3]
		plot_color.append('bs')
		plot_color2.append("b")
	elif statistics[i,4] == '0.0' and maximum_distance[i] <= 24: 
		statistics[i,4] = statistics[i,3]
		plot_color.append('m<')
		plot_color2.append("m")
	else:
		plot_color.append('ro')
		plot_color2.append("r")
	

print 'plot event time over obstacle density'	

fig1 = plt.figure(figsize =(6,4), dpi=300)
ax = fig1.add_subplot(111)
for i in range(len(statistics)):
	#print statistics[i][2]
	ax.plot(statistics[i,1], (float(statistics[i,4])/50.0)/60.0, plot_color[i])
ax.set_ylabel('time (min)')
ax.set_xlabel('obstacle density (%)')
ax.legend(handles=[red_patch, blue_patch, cyan_patch], fontsize='x-small')
#ax.set_ylim([-0.01, 0.1])
for i, txt in enumerate(statistics[:,0]):
    ax.annotate(txt, (statistics[i,1], (float(statistics[i,4])/50.0)/60.0), size = 2)
fig1.tight_layout()

fig1.savefig('../../data/'+run+'/plots/final/time_to_crash'+str(int(robot_size[0]*100))+str(int(robot_size[1]*100))+'.jpg', dpi = 300)

print 'plot event distance over obstacle density'	

fig2 = plt.figure(figsize =(6,4), dpi=300)
ax = fig2.add_subplot(111)
for i in range(len(statistics)):
	#print statistics[i][2]
	ax.plot(statistics[i,1], statistics[i,7], plot_color[i])
ax.set_ylabel('distance (m)')
ax.set_xlabel('obstacle density (%)')
ax.legend(handles=[red_patch, blue_patch, cyan_patch], fontsize='x-small')
ax.set_xlim([0, 35])
#for i, txt in enumerate(statistics[:,0]):
#    ax.annotate(txt, (statistics[i,1], statistics[i,7]), size = 2)
fig2.tight_layout()

fig2.savefig('../../data/'+run+'/plots/final/distance_to_crash'+str(int(robot_size[0]*100))+str(int(robot_size[1]*100))+'.jpg', dpi = 300)

print 'plot velocity over obstacle density'
    
fig3 = plt.figure(figsize =(6,4), dpi=300)
ax = fig3.add_subplot(111)
for i in range(len(statistics)):
	#print statistics[i][2]
	ax.plot(statistics[i,1], float(statistics[i,8])*50.0, plot_color[i])
	print "velocity: "
	print float(statistics[i,8])*50.0
ax.set_ylabel('velocity (m/s)')
ax.set_xlabel('obstacle density (%)')
ax.legend(handles=[red_patch, blue_patch, cyan_patch], fontsize='x-small')
#ax.set_ylim([0.0034, 0.0038])
fig3.tight_layout()
  
fig3.savefig('../../data/'+run+'/plots/final/velocity.jpg', dpi = 300)




statistics[:,9] = statistics[:,9].astype(float)/robot_size[0]
statistics[:,10] = statistics[:,10].astype(float)/robot_size[0]
y = []
x = []
for i in range(len(statistics)):
	if float(statistics[i,9]) <= 30:
		y = np.append(y, float(statistics[i,9]))
		x = np.append(x, float(statistics[i,1]))

xsorted = np.sort(x)
	
popt, pcov = curve_fit(func, x, y)


residuals = y- func(x, *popt)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((y-np.mean(y))**2)
r_squared = 1 - (ss_res / ss_tot)

black_patch = mpatches.Patch(color='black', label='curve fit, r2 ='+ str(r_squared.round(2)))



coef = np.polyfit(x,y,2)
poly1d_fn = np.poly1d(coef) 

print 'plot mean clearance over obstacle density'

fig4 = plt.figure(figsize =(6,4), dpi=300)
ax = fig4.add_subplot(111)
#ax.errorbar(statistics[:,1], statistics[:,9].astype(float), statistics[:,10].astype(float),linestyle='None', fmt='-', c = 'grey', )
for i in range(len(statistics[:,1])):
	ax.plot(statistics[i,1], statistics[i,9], plot_color[i])
ax.set_ylabel('mean clearance (a.u.)')
ax.set_xlabel('obstacle density (%)')
ax.legend(handles=[red_patch, blue_patch, cyan_patch, black_patch], fontsize='x-small')
#for i, txt in enumerate(statistics[:,0]):
#    ax.annotate(txt, (statistics[i,1], statistics[i,9]), size = 2)
plt.plot(xsorted, func(xsorted, *popt), '-', c ='k', label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))
ax.set_ylim([0, 45])
ax.set_xlim([0, 40])
fig4.tight_layout()
  
fig4.savefig('../../data/'+run+'/plots/final/obstacle_distance.jpg', dpi = 300)
  
#plt.show()
runs_no_collision_array = []

number_bins = 12

print 'plot success rate over obstacle density'

fig5 = plt.figure(figsize =(6,4), dpi=300)
ax = fig5.add_subplot(111)
for i in np.arange(0, max(statistics[:,1].astype(float)),max(statistics[:,1].astype(float))/number_bins):
	number_runs = 0
	runs_no_collision = 0
	for j in range(len(statistics[:,1])):
		if abs(i-float(statistics[j,1])) <= max(statistics[:,1].astype(float))/number_bins:
			number_runs = number_runs + 1
			#print number_runs
			if plot_color[j] != 'ro':
				runs_no_collision = runs_no_collision +1
				#print runs_no_collision
	if number_runs != 0:
		runs_no_collision_array.append(float(runs_no_collision)/float(number_runs)*100)
	else:
		runs_no_collision_array.append(0)
#print runs_no_collision_array

bars = ax.bar(np.arange(0, max(statistics[:,1].astype(float)),max(statistics[:,1].astype(float))/number_bins),runs_no_collision_array, max(statistics[:,1].astype(float))/number_bins -0.2)
ax.set_ylabel('success rate (%)')
ax.set_xlabel('obstacle density (%)')
ax.set_ylim([-10, 110])
ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
ax.grid()
fig5.tight_layout()
  
fig5.savefig('../../data/'+run+'/plots/final/collisions_percentage'+str(int(robot_size[0]*100))+str(int(robot_size[1]*100))+'.jpg', dpi = 300)


percentage = 0
for i in range(len(bars.patches)):
	percentage = percentage + bars.patches[i].get_height()
	
mean_success_rate = percentage/len(bars.patches)
print 'mean success rate: '
print mean_success_rate


print 'plot success and events over obstacle density'

fig8 = plt.figure(figsize =(6,4), dpi=300)
ax2 = fig8.add_subplot(211)
for i in range(len(statistics)):
	ax2.plot(statistics[i,1], (float(statistics[i,4])/50.0)/60.0, plot_color[i])
ax2.set_ylabel('time (min)')
#ax2.set_xlabel('obstacle density (%)')
ax2.legend(handles=[red_patch, blue_patch, cyan_patch], fontsize='x-small')
ax = fig8.add_subplot(212)
ax.bar(np.arange(0, max(statistics[:,1].astype(float)),max(statistics[:,1].astype(float))/number_bins),runs_no_collision_array, max(statistics[:,1].astype(float))/number_bins -0.2, color = 'k')
ax.set_ylabel('success rate (%)')
ax.set_xlabel('obstacle density (%)')
ax.set_ylim([-10, 110])
ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
ax.yaxis.set_major_locator(ticker.MultipleLocator(20))
ax.grid()
fig8.tight_layout()
  
fig8.savefig('../../data/'+run+'/plots/final/collisions'+str(int(robot_size[0]*100))+str(int(robot_size[1]*100))+'.jpg', dpi = 300)

if os.path.exists('../../data/'+run+'/statistics/turning_spikes_difference.npy') == True and os.path.exists('../../data/'+run+'/statistics/angles.npy') == True:
	turning_spikes_difference = np.load('../../data/'+run+'/statistics/turning_spikes_difference.npy')
	angles = np.load('../../data/'+run+'/statistics/angles.npy')
	print 'plot angles over turning spikes'
	fig6 = plt.figure(figsize =(6,4), dpi=300)
	ax = fig6.add_subplot(111)
	ax.plot(turning_spikes_difference, angles, '.b', ms = 2)
	ax.set_ylabel('|$\Delta$angle| (' + u'\N{DEGREE SIGN})')
	ax.set_xlabel('# spikes |left turn - right turn|')
	fig6.tight_layout()
	fig6.savefig('../../data/'+run+'/plots/final/turn_angle_spikes.jpg', dpi = 300)

	obstacle_density = np.load('../../data/'+run+'/statistics/obstacle_density.npy')
	bins = 10
	df = pd.DataFrame({'X' : obstacle_density.astype(float), 'Y' : angles})
	data_cut = pd.cut(df.X,bins)           #we cut the data following the bins
	grp = df.groupby(by = data_cut)        #we group the data by the cut
	ret = grp.aggregate(np.std)  
	ret2 = grp.aggregate(np.mean) 
	
	print 'plot delta angle over obstacle density'
	fig7 = plt.figure(figsize =(6,4), dpi=300)
	ax = fig7.add_subplot(111)
	ax.plot(obstacle_density, angles, '.b', ms = 2)
	ax.plot(ret2.X,ret.Y+ret2.Y,'r--',lw=2,alpha=.8)
	ax.plot(ret2.X,ret.Y,'r',lw=4,alpha=.8)
	ax.set_ylabel('|$\Delta$angle| (' + u'\N{DEGREE SIGN})')
	ax.set_xlabel('obstacle density (%)')
	fig7.tight_layout()
	fig7.savefig('../../data/'+run+'/plots/final/turn_angle_density.jpg', dpi = 300)

	bins = 10
	df = pd.DataFrame({'X' : obstacle_density.astype(float), 'Y' : turning_spikes_difference})
	data_cut = pd.cut(df.X,bins)           #we cut the data following the bins
	grp = df.groupby(by = data_cut)        #we group the data by the cut
	ret = grp.aggregate(np.std)  
	ret2 = grp.aggregate(np.mean)  
	print 'plot turning spikes over obstacle density'
	fig8 = plt.figure(figsize =(6,4), dpi=300)
	ax = fig8.add_subplot(111)
	ax.plot(obstacle_density, turning_spikes_difference, '.b', ms = 2)
	ax.plot(ret2.X,ret.Y+ret2.Y,'r--',lw=2,alpha=.8)
	ax.plot(ret2.X,ret.Y,'r',lw=4,alpha=.8)
	ax.set_ylabel('# spikes |left turn - right turn|')
	ax.set_xlabel('obstacle density (%)')
	fig8.tight_layout()
	fig8.savefig('../../data/'+run+'/plots/final/spikes_difference_density.jpg', dpi = 300)




