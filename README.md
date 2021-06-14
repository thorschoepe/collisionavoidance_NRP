# collision avoidance in the neurorobotics platform (NRP)

This repository helps you to set up and run a collision avoidance experiment with spiking neural networks in the Neurorobotics Platform (NRP).
This simulation environment has been used by https://arxiv.org/abs/2102.08417.
First of all download the folder named "code" which includes most of the files mentioned below. 

## 1. NRP installation


So far this experiment has been executed on Ubuntu 16.04 LTS with the NRP version 2.3.
A short test has also been run with Ubuntu 18.04 LTS.
Use the same environment, if you want to be sure to run into no bugs.
Since we have to modify and add a few files to the NRP you can't use the NRP servers.
You have to do a local from source install on your computer. An installation
manual is given here:

https://www.neurorobotics.net/ 


## 2. NRP modifications

After you have finished the local NRP from source install following the instructions at the link above you have to modify some parts of the platform.

### 2.1 Dynamic Vision Sensor (DVS) model

You have to add the DVS model to the NRP since 
the spikebot uses the DVS as sensor.
This model is already included in newer NRP versions

Download all files from: 
https://github.com/HBPNeurorobotics/gazebo_dvs_plugin

Put all files into the catkin workspace directory:
NRP/GazeboRosPackages/src/gazebo_dvs_plugin/
(If the folder gazebo_dvs_plugin doesn't exist until now, create it.)

run in user-scripts:
./configure_nrp

run in user-scripts:
./update_nrp build all 

### 2.2 Spikebot model

You have to add the spikebot model to your NRP install at the two following paths:

NRP/Models:

Add a folder called spikebot including the .config and .sdf file of 
the spikebot model which can be found at:
collisionavoidance_NRP/code/spikebot_model/


NRP/Models/robots/:

Add a folder called spikebot including the .config and .sdf file of 
the spikebot model which can be found at:
collisionavoidance_NRP/code/spikebot_model/


### 2.3 Obstacle texture

If you use the state machine function states.SpawnBox from NRP/ExperimentControl/hbp_nrp_excontrol/hbp_nrp_excontrol/nrp_states/_ModelServiceState.py
and you want to add a specific texture to the boxes you have to refer to a script defining the texture.
The location of the "texture.material" script should be added at line 117 in _ModelServiceState.py.
For example like this:
                
                + '        <material><script>' \
                + '           <uri>/home/neuro/.gazebo/models/grating_wall/materials/scripts/</uri>' \
                + '           <name>' + color + '</name>' \
                + '        </script></material>' \

The folder scripts contains the texture.material file which defines the new texture of the box.
The file contains this:

	material RepeatedTexture
	{
	  technique
	  {
		pass
		{
		  texture_unit
		  {
			// Relative to the location of the material script 
			texture ../textures/grating2.jpg
			// Repeat the texture over the surface (4 per face)
			scale 0.5 0.5
		  }
		}
	  }
	}

The script takes the material grating2.jpg at the location relative to the script ../textures/grating2.jpg
and repeates the texture four times over each surface. The material has to be called with the name "RepeatedTexture"

### 2.4 State machine modifications

Unfortunately, some of the state machine plugins
are not correctly referred  to in the _init__.py file. Because of that you have 
to replace the _init__.py file at the NRP location
NRP/ExperimentControl/hbp_nrp_excontrol/hbp_nrp_excontrol/nrp_states/

with the _init__.py file given at:

collisionavoidance_NRP/code/nrp_modified/


After that the state machine which is used to create a random environment
and monitors, if the robot craches into any object or left the arena, should 
work flawlessly. 


### 2.5 sEMD/TDE nest model

Since the spikebot brain is using the nest version of the spiking elementary motion detector/Time difference encoder you have to add this model to the nest environment.

The nest sEMD/TDE model and a test script for a single sEMD can be found at:
collisionavoidance_NRP/code/nest_semd_model/
To add this model to the nest environment follow these instructions, but first read the ATTENTION
text below: 
https://nest.github.io/nest-simulator/extension_modules

ATTENTION: Since the neurorobotics platform installs nest to .local the nest install path is:

export NEST_INSTALL_DIR=~/.local

export LIBRARY_PATH=~/.local/lib:$LIBRARY_PATH

export LD_LIBRARY_PATH=~/.local/lib/nest/:$LD_LIBRARY_PATH



## 3. Use the NRP platform

Open a terminal and run:

cle-nginx
cle-start

When the messages in the terminal don't change anymore, enter your browser and go to:

http://localhost:9000/#/esv-private?dev

username: nrpuser
password: password

The steps above are also explained on the NRP webpage

To add the latest NRP spikebot experiment go to "My experiments" -> Import zip
Upload the zip file from:

collisionavoidance_NRP/code/experiments/spikebot_cluttered_environment.zip

You can run any version directly in the browser by simply going to My experiments, clicking on the experiment and clicking Launch.
If you launch the experiment the first time the script random_experiment.exd will complain that the file number_experiment.npy
does not exist. In case you do not use the automated environment you can just set num=0 in line 36, 81 and 94 of the script random_environment.exd.
If you want to execute a series of experiments combined with statistical analysis I recommend the environment I created explained
in section 4 below.



## 4. Use the automated environment I have created for statistics and running experiments


If you want to use the automated environment for executing the simulations, statistics
and saving data, copy the folder"code" with all its content to a subdirectory of your choice.
Then, you create the following subdirectories. You open a terminal while being in the folder "code".

cd ..
mkdir data
cd data
mkdir "run_folder"
cd "run_folder"

The variable "run_folder" is the name of the folder in which all data of the current NRP run will be saved.
You can choose the name of the folder yourself. For more explanation see below.

In the folder "run_folder" create these subfolders:

mkdir plots
mkdir rawdata
mkdir statistics
mkdir world_objects_coordinates
cd plots
mkdir final
mkdir spikes
mkdir trajectories
mkdir turning_angles
mkdir clearance_calculation
mkdir angle
cd ../world_objects_coordinates
mkdir final
mkdir tmp

This environment is using the virtual_coach, an NRP program for automatized NRP experiment execution,
combined with various python scripts I wrote myself. Before you can execute the virtual_coach to run
your experiment you have to add the experiment you want to execute to the NRP environment and define a few variables.

### 4.1 Add an experiment

To add the experiment you want to execute to the NRP open a terminal and run:

cle-nginx
cle-start

When the messages in the terminal don't change anymore, enter your browser and go to:

http://localhost:9000/#/esv-private?dev

username: nrpuser
password: password

The steps above are also explained on the NRP webpage

To add the NRP spikebot experiment of your choice go to "My experiments" -> Import zip
You can use this zip file as a start point:

collisionavoidance_NRP/code/experiments/spikebot_cluttered_environment.zip

After you've added the experiment to the NRP it will be given a name.
You can see the name in the browser at Experiment files, Experiments on the left side panel.
You have to set this name as the "run_name" variable string in step 4.2 below.


### 4.2 Set up the environment

Two variables have to be set for each experiment, the name of the experiment "run_name"
and the name of the folder where the data will be saved "run_folder". You set both of these
variables in the script code/virtual_coach/number_collision_avoidance.py
Always check before running that the variable name fits the required destination.
You can set the "run_folder" variable and the "run_name" variable as an array in code/virtual_coach/number_collision_avoidance.py.
Then, the code will automatically run all these experiments one after the other. The number of repetitions of each experiment is defined
in number_collision_avoidance.py within the variable "number_repetitions".

Before running the experiment make sure that all path variables are set correctly. Hence, check all files in the experiment zip, and the folder code/virtual_coach for wrong path variables.


### 4.3 Run the automated environment (virtual coach)

To run the virtual coach execute: 
source ~/.opt/platform_venv/bin/activate
python collision_avoidance.py

At the beginning of the run the obstacle locations are saved to "data/"run_folder"/world_objects_coordinates/tmp/objects_tmp".
When the simulation finishes the data are saved to the final location "data/"run_folder"/world_objects_coordinates/final/". The filename includes
the datetime when the file was saved. After that the objects_tmp file is deleted.
During the simulation the robot's trajectory and spike data are saved to: ~/.opt/nrpStorage/"run_name"/.
When the simulation finshes these data will be copied to "data/"run_folder"/rawdata/". The filename includes the datetime similar to the world_objects_coordinates
file so that both files can be correlated in the statistics analysis part.
It might happen that the simulation breaks down after a few runs because of some errorcode 500. This is probably related to the state machine in random_environment.py
not finishing properly. Always make sure that the stopping time in random_environment.py's state machine "check_time" is lower than the timeout value in 
experiment_configuration.exc. This probably prevents crashes due to the state machine not stopping properly.


## 5. Analysis

I've created a few scripts to characterize and plot the data afterwards. (code/statistics/, code/plots)
You can execute all of these scripts at once by running the code "run_modules.py" at:
code/run_modules/run_modules.py
Before doing that you have to set the "run_folder" variable in "code/run_modules/number_run.py".
This variable defines which data from which folder will be analyzed.
The data analysis might take a few hours depending on the amount of data you have collected.
