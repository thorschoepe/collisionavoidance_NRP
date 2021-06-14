import sys
import numpy as np
import matplotlib.pyplot as plt
import itertools
import os
import re
from datetime import datetime
import math
import matplotlib.patches as mpatches

sys.path.append("../../data/arena_all/statistics/")
from arena_data import data

Data, plots = data()

distance_wall = np.load("../../data/arena_all/statistics/distance_wall.npy")

red_patch = mpatches.Patch(color='m', label='tau fac: 5')
black_patch = mpatches.Patch(color='c', label='tau fac: 100')
blue_patch = mpatches.Patch(color='orange', label='tau fac: 50')


fig1 = plt.figure(figsize =(6,6), dpi=300)
ax1 = fig1.add_subplot(111)
colour = ['m', 'c', 'orange']

for plot in range(3):
	data_x = []
	data_y = []
	data_xlabel = []
	for experiment in range(len(plots[plot][1])):
		for i in range(len(Data.run)):
			for distance in range(len(distance_wall)):
				if plots[plot][1][experiment] == Data.run[i] and distance_wall[distance][0] == Data.run[i]:
					data_x.append(plots[plot][0][i])
					data_y.append(distance_wall[distance][1])
					data_xlabel = plots[plot][2]
	lists = sorted(itertools.izip(*[data_x, data_y]))
	data_x, data_y = list(itertools.izip(*lists))
	ax1.plot(data_x, data_y, colour[plot])
	ax1.plot(data_x, data_y, '.k', ms = 8)
	ax1.set_xlabel(data_xlabel)
	ax1.set_ylabel('mean wall clearance')
	ax1.set_ylim([1,2.2])
	ax1.set_xlim([min(data_x)-((max(data_x)-min(data_x))/10.0), max(data_x)+((max(data_x)-min(data_x))/10.0)])
	ax1.legend(handles=[black_patch, blue_patch, red_patch], fontsize='small')
	fig1.savefig('../../data/arena_all/plots/distance_wall/plot_clearance_saccadic_speed.jpg', dpi = 300)
