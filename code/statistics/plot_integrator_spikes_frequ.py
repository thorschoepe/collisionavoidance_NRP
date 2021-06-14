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

int_spike_frequ = np.load('../../data/'+run+'/statistics/integrators_spike_frequency.npy')
fig1 = plt.figure(figsize =(6,5), dpi=300)
ax = fig1.add_subplot(111)
ax.plot(int_spike_frequ[:,1],np.divide(int_spike_frequ[:,2].astype(float), 128.0), '.b')
ax.set_ylabel('frequency (Hz)')
ax.set_xlabel('obstacle density (%)')
#plt.show()
fig1.savefig('../../data/'+run+'/plots/final/integrator_frequency.jpg', dpi = 300)
