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

path_files = '../../data/'+run+'/world_objects_coordinates/final/'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path_files):
    for file in f:
        if '.npy' in file:
            files.append(file)
            
print 'loaded files'
            
def skipper(fname):
    with open(fname) as fin:
        no_comments = (line for line in fin if not line.lstrip().startswith('#'))
        next(no_comments, None) # skip header
        for row in no_comments:
            yield row
            


for i in range(len(files)):
 files[i] = re.sub('\.npy$', '', files[i])
 
print 'sort files'

files.sort(key = lambda date: datetime.strptime(date, '%Y-%m-%d_%H_%M'))

statistics = np.load('../../data/'+run+'/statistics/statistics.npy')

spike_frequency = []

for idx in range(len(files)):
	
		recording = 'csv_records_' + files[idx]
		path = '../../data/'+run+'/rawdata/'+recording+'/'
		
		print 'load spikes'
		integrator_rl = np.loadtxt(skipper(path + 'integrator_rl_spikes.csv'), delimiter=",", usecols = (0,1))
		integrator_lr = np.loadtxt(skipper(path + 'integrator_lr_spikes.csv'), delimiter=",", usecols = (0,1))
		
		#print integrator_lr

		print 'calculate frequency'
		spike_frequency.append([statistics[idx,0], statistics[idx,1], (len(integrator_rl[:,0])+len(integrator_lr[:,0]))/((max(max(integrator_rl[:,1]),max(integrator_lr[:,1]))-min(min(integrator_rl[:,1]),min(integrator_lr[:,1])))/1000)])
		print spike_frequency
		np.save('../../data/'+run+'/statistics/integrators_spike_frequency.npy', spike_frequency)
	

