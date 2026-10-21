#!/bin/bash
# ArduPilot Rover SITL setup: stock motorboat, Rover-4.7.2. Run on a fresh Ubuntu 22.04.
set -e

cd ~
git clone --recurse-submodules https://github.com/ArduPilot/ardupilot.git
cd ardupilot
git checkout Rover-4.7.2
git submodule update --init --recursive

Tools/environment_install/install-prereqs-ubuntu.sh -y
. ~/.profile

cd ~/ardupilot
./waf configure --board sitl
./waf rover

mkdir -p ~/.config/ardupilot
grep -q "^LAKE=" ~/.config/ardupilot/locations.txt 2>/dev/null || \
  echo "LAKE=36.5986135,-121.8689162,0,0" >> ~/.config/ardupilot/locations.txt

cd ~/ardupilot/Rover
../Tools/autotest/sim_vehicle.py -f motorboat --map --console -L LAKE
