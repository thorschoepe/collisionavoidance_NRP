import numpy as np
import matplotlib.pyplot as plt
import os


path_files = '../../data/arena_all/plots/turns_over_distance/rawdata/'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path_files):
	for file in f:
		if '.npy' in file:
			files.append(file)

data = []	
	
for i in range(len(files)):
	data.append(np.load(path_files+files[i]))

polynomial = []
x_polynomial = []

for i in range(len(data)):
	polynomial.append(np.poly1d(np.polyfit(data[i][0],data[i][1] , 3)))
	x_polynomial.append(np.arange(np.amin(data[i][0]), np.amax(data[i][0]) , 0.01))

data_y = []

fig = plt.figure(figsize =(6,5), dpi=300)
ax = fig.add_subplot(111)	
for i in range(len(data)):
	ax.plot(data[i][0],data[i][1], '.')
	data_y = np.append(data_y, data[i][1])
for i in range(len(data)):
	ax.plot(x_polynomial[i], polynomial[i](x_polynomial[i]), '-k')

ax.set_ylim([np.amin(data_y), np.amax(data_y)])
ax.set_ylabel('turn (rad/sec)')
ax.set_xlabel('distance (m)')
plt.yscale('log')
plt.tight_layout()
fig.savefig('../../data/arena_all/plots/turns_over_distance/turn_over_distance_all.jpg', dpi = 300)


plt.show()
