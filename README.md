# `pyvale` Hackathon May 2025
Welcome to the `pyvale` hackathon for May 2025.

## Cloning this Repository
First clone this repository to your home directory using:
```shell
git clone git@github.com:Computer-Aided-Validation-Laboratory/hackathon-may-2025.git
```

Now create your own branch using, replacing "YOURINTIALS" with your initials:
```shell
git checkout -b "YOURINITIALS"
```





## Installing `pyvale`: Ubuntu
We are going to work in an editable installation of `pyvale` so that we can push hot fixes and edit the code if needed. If you already know how to install an editable version of a python package into a virtual environment then all you need to do is clone `pyvale` from [here](https://github.com/Computer-Aided-Validation-Laboratory/pyvale) and then switch to the dev branch. If you would like a bit more detailed guidance then read on.

### Managing Python Versions
To be compatible with `bpy` (the Blender python interface), `pyvale` uses python 3.11. To install python 3.11 without corrupting your operating systems python installation first add the deadsnakes repository to apt:
```shell
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update && sudo apt upgrade -y
```

Install python 3.11:
```shell
sudo apt install python3.11
```

Add `venv` to your python 3.11 install:
```shell
sudo apt install python3.11-venv
```

Check your python 3.11 install is working using the following command which should open an interactive python interpreter, as long as it open everything is working and you can close it with `quit()`:
```shell
python3.11
```

### Cloning `pyvale` from Github
Navigate to the `pyvale` [github page](https://github.com/Computer-Aided-Validation-Laboratory/pyvale) and open a terminal in your home directory to clone `pyvale`:

```shell
git clone git@github.com:Computer-Aided-Validation-Laboratory/pyvale.git
```

Navigate to the `pyvale` directory and switch to the dev branch:
```shell
cd pyvale
git switch dev
```

Double check you are on the dev branch as this is where we will push hotfixes:
```shell
git branch
```

When we push a hotfix to the dev branch you will need to pull it down from the repository:
```shell
git pull
```

### Virtual Environment & Editable Install
We recommend installing `pyvale` in a virtual environment using `venv`. Navigate  to the `pyvale` directory if you are not there already and run:

```shell
python3.11 -m venv .env
source .venv/bin/activate
```

As we are in the `pyvale` directory and our virtual environment is activated we can add an editable install to our virtual environment using:

```shell
pip install -e .
```

If you are using Visual Studio Code then set your python interpreter to use this virtual environmentn using ctrl+shift+p to open the command pallete and search for 'Python: Select Interpreter'.

### Checking Your `pyvale` Install
If everything has worked correctly you should be able to run python from within your virtual environment (should open a python 3.11 interpreter):
```shell
python
```

Now you should be able to import `pyvale`:
```python
import pyvale
```

If you don't get any errors you are ready to look at the examples!

## Part 1: `pyvale` Examples
You can find the `pyvale` point sensor examples [here](https://computer-aided-validation-laboratory.github.io/pyvale/examples/point/point.html) as part of the `pyvale` documentation. Work through these examples starting with the first one [here](https://computer-aided-validation-laboratory.github.io/pyvale/examples/point/ex1_1.html). If you find any bugs let us know! Feel free to experiment with the examples by turning things on/off as well as mixing and matching different components of the `pyvale` sensor simulation system.

## Part 2: Hacking `pyvale` Point Sensors
Here are a series of challenges for using `pyvale` to simulate sensors to consolidate what you have learned from the examples. The inputs for each case are exodus outputs from MOOSE simulations so you might want to open them in paraview to have a look at the fields before doing anything. You can download [paraview here](https://www.paraview.org/download/). You don't need to do the challenges in order and feel free to BYO challenge - if you need help getting MOOSE working or you have a simulation you want to mess around with go for it! You can also combine your BYO challenge with some of the suggestions below if you like. If you feel like you need a bit more of a guided challenge then just use the challenges below

All simulation outputs for the challenges below can be found [here](https://ukaeauk-my.sharepoint.com/:f:/g/personal/lloyd_fletcher_ukaea_uk/EsVjHWx50S9DjnCKXpD0tlkBALkml8Py1MPArjHWbwbtfw?e=iihhyG). The simulation input files can be found [here](https://github.com/Computer-Aided-Validation-Laboratory/hackathon-may-2025/tree/main/sims) but try not to cheat and look at the input material properties before doing challenge 1.


### Challenge 1: A Dogbone Tensile Test
For this case you have been given a simulation of a standard tensile test on a dogbone sample and have been given the following challenges:
- Create a simple point tracking displacement sensor using `pyvale` with vector fields.
- Create an extensometer type strain sensor by hacking together `pyvale` point displacement sensors.
- Create a strain gauge sensor.
- Create a load cell sensor by hacking `pyvale` vector field sensors (hint: you have the stress fields in the simulation output)
- For each of the sensors you have built add an error chain
- Use your hacked load cell and extensometer to plot the simulated stress strain curves with uncertainty bounds. Here the experiment simulation module should help.
- Use your stress strain curve to give predicted uncertainties for the elastic modulus, yield strength and hardening modulus.
- Which error sources contribute the most to the uncertainty on the derived parameters from the stress strain curves?
- **Extension**: create a simplified digital image correlation displacement sensor using a dense grid of point displacement sensors. Then see if you can mimic the DIC strain calculation window by hacking the displacement point sensors with some post processing.

See if you can complete the above challenges without looking at the simulation input file which contains the nominal material properties.


### Challenge 2: Sensor Placement Optimisation
For this challenge you been provided a series of three simulations:
1. Thermal, 2D: rectangular plate with a bi-directional temperature gradient.
2. Mechanical, 3D: linear elastic rectangular plate with a hole loaded in tension.
3. Thermo-Mechanical, 3D: 3 material monoblock with a surface heat flux and active cooling, mechanical deformation results from thermo-mechanical coupling.

Your task is to develop a sensor placement optimisation algorithm to determine the minimum number of sensors to reconstruct the given fields (temperature, displacement, strain) with a given level of precision and accuracy (5% is a good starting point). You can also investigate the minimum number of sensors required to predict the field maximum or minimu with a 5% error. Start with perfect sensors with no errors and then start adding errors and performing stochastic optimisation.

For the 2nd simulation for the plate with a hole the challenge is to predict the stress concentration factor for the plate with the minimum number of strain gauges. You will need Roark's formulas for stress and strain which is in the

**Hints:**
- Start with the 2D plate as it is easy to reason about, is only a scalar field
- For field reconstruction from sparse sensor data I would look at Gaussian processes and radial basis functions both of which can be found in the python package `scikit-learn`. If you want to try something more challenging try using principal component analysis combined with gaussian processes.
- For the optimisation algorithm I would start with Nelder-Mead from `scipy.optimize` but it doesn't parallelise well. If you want a gradient free optimiser like a genetic algorithm or particle swarm then try `pymoo`
- For the cost function I would start witth something simple like the root mean square error over all nodes of the simulation based on the function you have fitted to the sensor values. If you want something more interesting look into information entropy and expected information gain.


### Challenge 3: Inverse Identification
NOTE: For this challenge you will need a MOOSE installation and Gmsh along with `mooseherder`. If you need help installing MOOSE let us know.

For this challenge you been provided a series of three simulations:
1. Thermal, 2D: rectangular plate with a bi-directional temperature gradient.
2. Mechanical, 3D: linear elastic rectangular plate with a hole loaded in tension.
3. Thermo-Mechanical, 3D: 3 material monoblock with a surface heat flux and active cooling, mechanical deformation results from thermo-mechanical coupling.

Your task is to develop an inverse identification algorithm to identify a material property or boundary condition of your choice from each simulation by coupling `mooseherder` with the point sensor capability of `pyvale`. Start with perfect sensors and then develop your algorithm further to include errors and stochastic optimisation.

**Hints**
- For the optimisation algorithm I would start with Nelder-Mead from `scipy.optimize` but it doesn't parallelise well. If you want a gradient free optimiser like a genetic algorithm or particle swarm then try `pymoo`.




