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
python -m pip install pygame
python -m pip install pynput
python -m pip install --upgrade pip
python -m pip install --upgrade Pillow

python3.6 -m pip install gtts
python3.6 -m pip install imutils
python3.6 -m pip install pexpect
python3.6 -m pip install gTTS
python3.6 -m pip install selenium
python3.6 -m pip install pynput

sudo apt-get install git cmake libpython3-dev python3-numpy mpg321 chromium-chromdriver nano 
cd ~
git clone --recursive https://github.com/dusty-nv/jetson-inference
cd jetson-inference
mkdir build
cd build
cmake ../
make
sudo make install
sudo ldconfig

if cat /lib/systemd/system/bluetooth.service.d/nv-bluetooth-service.conf | grep -q "noplugin"
then
	echo $'\nConfiguring Bluetooth'
	sudo cp nv-bluetooth-service.conf /lib/systemd/system/bluetooth.service.d
	sudo systemctl daemon-reload
	sudo systemctl restart bluetooth
else
	echo $'\nBluetooth configured'
fi

echo $'\nConfiguring startup scripts'
mkdir ~/.config/autostart
cp start_UI.desktop ~/.config/autostart
cp start_detection.desktop ~/.config/autostart

echo $'\nActivating fan service'
sudo cp start_fan.service /etc/systemd/system/
sudo chmod 664 /etc/systemd/system/start_fan.service
sudo systemctl daemon-reload
sudo systemctl enable start_fan.service
