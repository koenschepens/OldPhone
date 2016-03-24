#!/bin/sh

#now=$(date +"%m_%d_%Y_%T")
#echo "********* update.sh **********" >> ~/keypadUpdater2.log

sudo service mediacenter stop
#sudo git pull
sudo ./install.sh -f
sudo service mediacenter start