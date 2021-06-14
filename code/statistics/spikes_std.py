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

statistics = np.load('../../data/'+run+'/statistics/statistics.npy')
spikes_wta_mean = np.load('../../data/'+run+'/statistics/spikes_wta_mean.npy')
spikes_wta_std = np.load('../../data/'+run+'/statistics/spikes_wta_std.npy')

obstacle_density = []
spike_wta_mean = []
spike_wta_std = []



for i in range(len(statistics)):
	for j in range(len(spikes_wta_mean)):
		if statistics[i,0] == spikes_wta_mean[j]:
			spike_wta_mean = np.append(spike_wta_mean,spikes_wta_mean[j-1])
			spike_wta_std = np.append(spike_wta_std,spikes_wta_std[j-1])
			obstacle_density = np.append(obstacle_density, statistics[i,1])
		

fig = plt.figure(figsize =(6,4), dpi=300)
ax = fig.add_subplot(111)
ax.plot(obstacle_density.astype(float),spike_wta_std.astype(float), '. b',  ms = 5)
ax.set_ylabel('std wta direction')
ax.set_xlabel('obstacle density (%)')

#plt.show()

fig.tight_layout()
fig.savefig('../../data/'+run+'/plots/spikes_stdd.jpg', dpi = 300)
	

		
