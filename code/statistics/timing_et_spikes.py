
# script to calculate duration from ending saccade until an et spike would be released

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


def closest(lst, K): 
	lst2 = [i for i in lst if i < K]
	lst2 = np.asarray(lst2) 
	#print lst2
	if lst2 != []:
		idx = (K - lst2).argmin() 
		return K- lst2[idx]
	else:
		return -1000


def skipper(fname):
    with open(fname) as fin:
        no_comments = (line for line in fin if not line.lstrip().startswith('#'))
        next(no_comments, None) # skip header
        for row in no_comments:
            yield row


et_spikes = np.loadtxt(skipper('/home/neuro/Documents/spiking-insect-vision/docs/nrp_collision_avoidance/data/run_57_clutter_checkerboard/rawdata/csv_records_2020-12-08_01_32/et_spikes.csv'), delimiter=",", usecols = (0,1))
oszi_1_spikes = np.loadtxt(skipper('/home/neuro/Documents/spiking-insect-vision/docs/nrp_collision_avoidance/data/run_57_clutter_checkerboard/rawdata/csv_records_2020-12-08_01_32/oszillator_1_spikes.csv'), delimiter=",", usecols = (0,1))
oszi_2_spikes = np.loadtxt(skipper('/home/neuro/Documents/spiking-insect-vision/docs/nrp_collision_avoidance/data/run_57_clutter_checkerboard/rawdata/csv_records_2020-12-08_01_32/oszillator_1_spikes.csv'), delimiter=",", usecols = (0,1))
wat_spikes = np.loadtxt(skipper('/home/neuro/Documents/spiking-insect-vision/docs/nrp_collision_avoidance/data/run_57_clutter_checkerboard/rawdata/csv_records_2020-12-08_01_32/wta_spikes.csv'), delimiter=",", usecols = (0,1))
#print et_spikes[:,1]

deltas_et = []

for i in range(len(et_spikes[:,1])):
	delta_et = min(closest(oszi_2_spikes[:,1],et_spikes[i,1]), closest(oszi_1_spikes[:,1],et_spikes[i,1]))
	if closest(wat_spikes[:,1],et_spikes[i,1]) > delta_et:
		deltas_et.append(delta_et)
		
print np.mean(deltas_et)
		

		
