# `pyvale` Hackathon May 2025
Welcome to the `pyvale` hackathon for May 2025.

## Installing `pyvale`
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

Check your python 3.11 install is working using the following command which should open an interactive python interpreter:
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

When we push hotfix to the dev branch you will need to pull it down from the repository:
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
If everything has worked correctly you should be able to run python from within your virtual environment:
```shell
python
```

Now you should be able to import `pyvale`:
```python
import pyvale
```

If you don't get any errors you are ready to look at the examples!

## Part 1: `pyvale` Examples
You can find the `pyvale` point sensor examples [here](https://computer-aided-validation-laboratory.github.io/pyvale/examples/point/point.html) as part of the `pyvale` documentation. Work through these examples starting with the first one [here](https://computer-aided-validation-laboratory.github.io/pyvale/examples/point/ex1_1.html).

## Part 2: Hacking `pyvale` Point Sensors
Here are a series of challenges for using `pyvale` to simulate sensors to test what you have learned from the examples.

### Challenge 1: The Simple Test Case


### Challenge 2: A Dogbone Tensile Test


### Extension, Challenge 3: Sensor Placement Optimisation
