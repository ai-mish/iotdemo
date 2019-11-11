#!/bin/bash

# Download the Linux Anaconda Distribution
wget https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh -O ~/anaconda3.sh

# Run the installer
bash ~/anaconda3.sh -b -p $HOME/anaconda3

### Run the conda init script to setup the shell
echo ". $HOME/anaconda3/etc/profile.d/conda.sh" >> $HOME/.bashrc
. $HOME/anaconda3/etc/profile.d/conda.sh
source $HOME/.bashrc

# Create a base Python3 environment separate from the base env
#conda create -y --name python3

# Install necessary Python packages
#conda activate python3

git clone https://github.com/sukmmi/iotdemo
conda env create --file iotdemo/conda/iotdemo.yaml
#conda env create --file conda2.yaml
#conda env update --file iotdemo/conda/iotdemo.yaml
conda activate iotdemo
echo "conda activate iotdemo" >> ~/.bashrc
