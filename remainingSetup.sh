#!/bin/bash

if pyenv versions | grep -q "3.10.0"
then
	echo $'\nPython 3.10.0 already installed'
else
	echo $'\nInstalling Python 3.10.0'
	pyenv install -v 3.10.0
fi

pyenv global 3.10.0

echo $'\nEnsuring correct python version:'
python -V
echo $'\nUpgrading pip:'
~/.pyenv/versions/3.10.0/bin/python -m pip install --upgrade pip
echo $'\nBeginning necessary library installation:'
python -m pip install wheel
python -m pip install pexpect
python -m pip install wifi
python -m pip install customtkinter
python -m pip install kivy

