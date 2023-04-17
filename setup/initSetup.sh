#!/bin/bash

echo 'Editing sudoers file to allow for all functions to occur without password entry'
echo 'Please enter you password once now'
if sudo grep -q "NOPASSWD" /etc/sudoers
then
	echo 'User already has sudo permissions'
else
	sudo sed 's/%sudo	ALL=(ALL:ALL) ALL/%sudo	ALL=(ALL:ALL) NOPASSWD: ALL/' /etc/sudoers | (sudo EDITOR='tee' visudo)
fi

echo Installing necessary libraries for pyenv
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl

echo $'\nDownloading pyenv'
curl https://pyenv.run | bash

echo $'\nEnsuring necessary lines in bashrc:'
if grep -q "pyenv" ~/.bashrc
then
	echo pyenv already in bashrc
else
	echo appending pyenv to bashrc
	cat ./bashrcLines.txt >> ~/.bashrc
fi

echo $'\nEnsuring necessary lines in profile:'
if grep -q "pyenv" ~/.profile
then
	echo pyenv already in profile
else
	echo appending pyenv to profile
	cat ./profileLines.txt >> ~/.profile
fi

exec ./remainingSetup.sh
