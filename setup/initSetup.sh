#!/bin/bash

if sudo grep -q "NOPASSWD" /etc/sudoers
then
	echo 'User already has sudo permissions'
else
	echo 'Adding permissions'
	sudo echo '$USER All=(ALL) NOPASSWD: ALL' >> /etc/sudoers
	echo 'sudoers will open now. Replace $USER with your name'
	read -p 'Press enter to continue';echo
	sudo visudo -f /etc/sudoers
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

exec $SHELL
