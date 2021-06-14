#script for executing simualtions in the NRP with the virtual code
# to run the script execute 'cle-virtual-coach python collision avoidance'
# Before that activate the NRP in a second terminal by typing cle-nginx, cle-start
# also activate the platform_venv environment by typing: source ~/.opt/platform_venv/bin/activate

import time
import os
import numpy as np
import shutil  
from datetime import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as patches
import matplotlib.cm as cm
import re
from matplotlib import image as img
import math
from scipy.spatial.distance import cdist
import sys
from number_collision_avoidance import number_ca 



#################################################################################################################################
run_folder, run_name, number_repetitions  = number_ca()


from hbp_nrp_virtual_coach.virtual_coach import VirtualCoach
vc = VirtualCoach(environment='local',storage_username='nrpuser',storage_password='password')
vc.print_available_servers()
vc.print_cloned_experiments()

for num in range(len(run_name)):
	
	np.save('../../data/number_experiment.npy', num)
	
	print 'run_folder: '
	print run_folder[num]

	for runs in range(number_repetitions[num]):	
			
		if os.path.exists('../../data/'+run_folder[num]+'/world_objects_coordinates/tmp/objects_tmp.npy') == True:
			os.remove('../../data/'+run_folder[num]+'/world_objects_coordinates/tmp/objects_tmp.npy')
		
		time.sleep(10)
		
		sim = vc.launch_experiment(run_name[num], server=None, reservation=None, cloned=True)
		
		
		time.sleep(60)
		
		sim.start()
		#sim.print_transfer_functions()


		time.sleep(10)

		sim.pause()
		

		time.sleep(60*5)

		sim.start()
		state = 'started'
		while state == 'started':
			state = sim.get_state()
		
		time.sleep(60)
		
		root = os.path.expanduser('~/.opt/nrpStorage/' + run_name[num])

		dirlist = [ item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item)) ]
		dirlist2 = []
		for i in range(len(dirlist)):
				if 'csv_records' in dirlist[i]:
					dirlist2.append(dirlist[i])



		for i in range(len(dirlist2)):
			dirlist2[i] = re.sub('csv_records_', '', dirlist2[i])


		dirlist2.sort(key = lambda date: datetime.strptime(date, '%Y-%m-%d_%H-%M-%S'))

		
		if os.path.exists('../../data/'+run_folder[num]+'/world_objects_coordinates/tmp/objects_tmp.npy') == True:
			object_name_time = datetime.now().strftime('%Y-%m-%d_%H_%M')
			src = root + '/csv_records_' + max(dirlist2)
			dest = '../../data/'+run_folder[num]+'/rawdata/csv_records_' + object_name_time
			shutil.copytree(src, dest)  
			obstacle_positions = np.load('../../data/'+run_folder[num]+'/world_objects_coordinates/tmp/objects_tmp.npy')
			np.save('../../data/'+run_folder[num]+'/world_objects_coordinates/final/'+object_name_time+'.npy', obstacle_positions)
			time.sleep(70)
			os.remove('../../data/'+run_folder[num]+'/world_objects_coordinates/tmp/objects_tmp.npy')
			
		time.sleep(600)

