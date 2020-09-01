#!/bin/sh

# Install pip
sudo apt-get install python-pip

# Install Python library
sudo pip install nfcpy colorzero
# enable users without sudo permisson
sudo sh -c 'echo SUBSYSTEM==\"usb\", ACTION==\"add\", ATTRS{idVendor}==\"054c\", ATTRS{idProduct}==\"06c3\", GROUP=\"plugdev\" >> /etc/udev/rules.d/nfcdev.rules'
sudo udevadm control -R

# make a data file
mkdir -p data/cards
touch data/cards/normal.dat
touch data/cards/auto_close.dat

# systemd
sudo cp key.service /etc/systemd/system/key.service
sudo systemctl daemon-reload
sudo systemctl enable key
