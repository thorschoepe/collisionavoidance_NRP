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

import matplotlib.pylab as pylab
params = {'legend.fontsize': 'x-large',
          'figure.figsize': (16, 4),
         'axes.labelsize': 26,
         'axes.titlesize':30,
         'xtick.labelsize':20,
         'ytick.labelsize':20}
pylab.rcParams.update(params)


plt.close('all')

def skipper(fname):
    with open(fname) as fin:
        no_comments = (line for line in fin if not line.lstrip().startswith('#'))
        next(no_comments, None) # skip header
        for row in no_comments:
            yield row


sEMD_rl = np.loadtxt(skipper('/home/neuro/Documents/spiking-insect-vision/docs/nrp_collision_avoidance/data/clutter_figure_1/rawdata/csv_records_2021-02-05_17_56/semd_rl_spikes.csv'), delimiter=",", usecols = (0,1))
sEMD_lr = np.loadtxt(skipper('/home/neuro/Documents/spiking-insect-vision/docs/nrp_collision_avoidance/data/clutter_figure_1/rawdata/csv_records_2021-02-05_17_56/semd_lr_spikes.csv'), delimiter=",", usecols = (0,1))
wta = np.loadtxt(skipper('/home/neuro/Documents/spiking-insect-vision/docs/nrp_collision_avoidance/data/clutter_figure_1/rawdata/csv_records_2021-02-05_17_56/wta_spikes.csv'), delimiter=",", usecols = (0,1))

sEMD_rl_transposed =  sEMD_rl.T
sEMD_lr_transposed =  sEMD_lr.T
wta_transposed = wta.T

#minimum_wta = min(wta_transposed[0])
minimum_wta = 3968
#minimum_semd_lr = min(sEMD_lr_transposed[0])
#minimum_semd_rl = min(sEMD_rl_transposed[0])
minimum_semd_lr = 2560
minimum_semd_rl = 1280
bins = 109
binsize = 10

sEMD_rl_t_x = []
sEMD_lr_t_x = []
sEMD_rl_t_y = []
sEMD_lr_t_y = []
wta_x = []

for i in range(len(wta_transposed[0])):
	if wta_transposed[1][i]/50 > bins-binsize/2 and wta_transposed[1][i]/50 < bins+binsize/2:
		wta_x.append(wta_transposed[0][i]-minimum_wta)

for i in range(len(sEMD_rl_transposed[0])):
	if sEMD_rl_transposed[1][i]/50 > bins-binsize/2 and sEMD_rl_transposed[1][i]/50 < bins+binsize/2:
		sEMD_rl_t_x.append(sEMD_rl_transposed[0][i]%64)
		sEMD_rl_t_y.append(19-((sEMD_rl_transposed[0][i]-sEMD_rl_transposed[0][i]%64)/64-minimum_semd_rl/64))
	
for i in range(len(sEMD_lr_transposed[0])):
	if sEMD_lr_transposed[1][i]/50 > bins-binsize/2 and sEMD_lr_transposed[1][i]/50 < bins+binsize/2:
		sEMD_lr_t_x.append(sEMD_lr_transposed[0][i]%64)
		sEMD_lr_t_y.append(19-((sEMD_lr_transposed[0][i]-sEMD_lr_transposed[0][i]%64)/64-minimum_semd_lr/64))

sEMD_both_t_x = []
sEMD_both_t_y = []
print len(sEMD_rl_t_x)
for i in range(len(sEMD_rl_t_x)):
	print i
	for y in range(len(sEMD_lr_t_x)):
		if sEMD_rl_t_x[i] == sEMD_lr_t_x[y] and sEMD_rl_t_y[i] == sEMD_lr_t_y[y]:
			sEMD_both_t_x.append(sEMD_lr_t_x[y])
			sEMD_both_t_y.append(sEMD_lr_t_y[y])
			

fig = plt.figure(figsize =(12,4), dpi=300)
ax = fig.add_subplot(111)
ax.plot(sEMD_rl_t_x, sEMD_rl_t_y, '.', c = 'darkorange', ms= 16)
ax.plot(sEMD_lr_t_x, sEMD_lr_t_y, '.', c = 'steelblue',  ms= 16)
ax.plot(sEMD_both_t_x, sEMD_both_t_y, '.', c = 'k',  ms= 16)
for i in range(len(wta_x)):
	ax.plot([wta_x[i],wta_x[i]],[-10, 30], c='m', lw=8)
ax.set_xlabel('Neuron ID')
ax.set_ylabel('Neuron ID')
ax.set_xlim([0,63])
ax.set_ylim([0,20])
fig.tight_layout()
fig.savefig('/home/neuro/Documents/spiking-insect-vision/docs/nrp_collision_avoidance/docs/sEMD_activity_'+str(bins)+'.png', dpi = 300)
