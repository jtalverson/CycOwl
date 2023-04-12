#!/bin/bash

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
	cat ~/CycOwl/bashrcLines.txt >> ~/.bashrc
fi

echo $'\nEnsuring necessary lines in profile:'
if grep -q "pyenv" ~/.profile
then
	echo pyenv already in profile
else
	echo appending pyenv to profile
	cat ~/CycOwl/profileLines.txt >> ~/.profile
fi

exec "$SHELL" & ./remainingSetup.sh
