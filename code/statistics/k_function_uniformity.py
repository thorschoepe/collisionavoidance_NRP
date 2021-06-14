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
from scipy.spatial.distance import euclidean
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches
import sys
sys.path.append("../run_modules/")
from number_run import number_run

run = number_run()

print 'k function'

red_patch = mpatches.Patch(color='red', label='collision')
blue_patch = mpatches.Patch(color='blue', label='no collision')
cyan_patch = mpatches.Patch(color='magenta', label='time over')

# figure out trial names, sort them 
path_files = '../../data/'+(run)+'/world_objects_coordinates/final/'

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

A = 30**2 # study region

	
statistics = np.load('../../data/'+run+'/statistics/statistics.npy')

plot_color = []
		
for i in range(len(statistics)):
	if statistics[i,4] == '0.0' and float(statistics[i,3]) > 50000.0:
		statistics[i,4] = statistics[i,3]
		plot_color.append('m')
	elif statistics[i,4] == '0.0' and float(statistics[i,3]) <= 50000.0:
		statistics[i,4] = statistics[i,3]
		plot_color.append('b')
	else:
		plot_color.append('r')
		
		
		

for h in range(1,17,2): # h: radius in which are objects
	
	print h
	
	if os.path.exists('../../data/'+run+'/statistics/Ks_h_'+str(h)+'.npy') == True:
		Ks = np.load('../../data/'+run+'/statistics/Ks_h_'+str(h)+'.npy')
	else:
		Ks = np.zeros([1,2])
	
	# calculate k value
	for idx in range(len(files)):
		objects = np.load('../../data/'+run+'/world_objects_coordinates/final/'+files[idx]+'.npy')
		N = len(objects) # number objects
		
		if files[idx] not in Ks[:,0]:
			# load obstacle coordinates
			K = 0
			
			
			lambda_ = float(N)/float(A)
			
			for i in range(N):
				for j in range(N):
					u = abs(euclidean([objects[i][0],objects[i][1]],[objects[j][0],objects[j][1]]))
					d1 = (15 -abs(objects[j][0]))
					d2 = (15 -abs(objects[j][1]))
					
					if u != 0:
						if u**2 <= d1**2 + d2**2 :
							w = 1 - math.pi**(-1) * (math.acos(min(d1,u)/u) + math.acos(min(d2,u)/u))
						else:
							w = 3/4 - (2* math.pi)**(-1) * (math.acos(d1/u) + math.acos(d2/u))
						
						
						if u <= h:
							K = lambda_**(-1) * w * u + K
			K = K/N
			Ks = np.concatenate((Ks,[[files[idx], K]]), axis = 0)
			#print 'Ks:' + str(Ks)
			if Ks[0,0] == '0.0':
			   Ks = np.delete(Ks, 0, 0)
				
			np.save('../../data/'+run+'/statistics/Ks_h_'+str(h)+'.npy',Ks)
	data = 0
	#print len(statistics)
	#print len(Ks)
	#print len(plot_color)
	data = np.concatenate(([statistics[:,1]],[Ks[:,1]],[statistics[:,4]],[plot_color],[np.divide(statistics[:,4].astype(float),float(5000))],[statistics[:,0]]), axis = 0)

	# Sort 2D numpy array by 2nd row
	data = data[:,data[4].argsort(kind='mergesort')]

	#print data

	#fig2 = plt.figure(figsize =(6,4), dpi=300)
	#ax = fig2.add_subplot(111, projection = '3d')
	#for i in range(len(Ks[:,1])):
		#ax.scatter(float(data[0][i]),float(data[1][i]), float(data[2][i])/30.0,c = data[3][i])
	#ax.set_ylim([3,6])
	##plt.show()
	#fig2.tight_layout()
	#fig2.savefig('/home/neuro/Documents/spiking-insect-vision/docs/nrp_collision_avoidance/data/plots/Ks_density_3d_h_'+str(h)+'.jpg', dpi = 300)

	fig3 = plt.figure(figsize =(6,4), dpi=300)
	ax = fig3.add_subplot(111)
	for i in range(len(Ks[:,1])):
		if data[3][i] == 'r' and float(data[1][i]) != 0.0: 
			ax.scatter(float(data[0][i]),float(data[1][i]),c = cm.Reds(np.divide(float(data[2][i])/30.0,float(max(data[2]))/30.0)))
		elif float(data[1][i]) != 0.0:
			ax.scatter(float(data[0][i]),float(data[1][i]),c = data[3][i])		
	for i, txt in enumerate(data[5][:]):
			ax.annotate(txt, (float(data[0][i]), float(data[1][i])), size = 2)
	#ax.set_ylim([3,5.5])
	ax.set_ylabel('K-factor')
	ax.set_xlabel('obstacle density (%)')
	ax.legend(handles=[red_patch, blue_patch, cyan_patch], fontsize='x-small')
	fig3.tight_layout()
	fig3.savefig('../../data/'+run+'/plots/Ks_density_2d_h_'+str(h)+'.jpg', dpi = 300)

	#fig4 = plt.figure(figsize =(6,4), dpi=300)
	#ax2 = fig4.add_subplot(111)
	#for i in range(len(data[0])):
		#ax2.scatter(float(data[1][i]), float(data[2][i])*30,c = data[3][i])
	#ax2.set_ylabel('time (s)')
	#ax2.set_xlabel('K-factor')
	##ax2.set_xlim([3,5.5])
	#ax2.legend(handles=[red_patch, blue_patch], fontsize='x-small')
	##plt.show()
	#fig4.tight_layout()
	#fig4.savefig('/home/neuro/Documents/spiking-insect-vision/docs/nrp_collision_avoidance/data/plots/Ks2d_h_'+str(h)+'.jpg', dpi = 300)



	
