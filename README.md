# VRE Tool Generator 

This Tool Generator is written for Python 3.7 and later.

* In order to install the dependencies you need `pip` and `venv` modules.
	- `pip` is available in many Linux distributions (Ubuntu packages `python3-pip`, CentOS EPEL package `python-pip`), 
	and also as [pip](https://pip.pypa.io/en/stable/) Python package.
	- `venv` is also available in many Linux distributions (Ubuntu package `python3-venv`). In some of them is 
	integrated into the Python 3.7 (or later) installation.

* The creation of a virtual environment where to install generic wrapper dependencies is done running:
```
python3 -m venv .pyWEenv
source .pyWEenv/bin/activate
pip install --upgrade pip wheel
pip install -r requirements.txt
```
* If you upgrade your Python installation (from version 3.7 to 3.8, for instance), or you move this folder to a different
location after following the instructions, you may need to remove and reinstall the virtual environment.