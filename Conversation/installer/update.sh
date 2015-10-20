#!/bin/sh

#now=$(date +"%m_%d_%Y_%T")
#echo "********* update.sh **********" >> ~/keypadUpdater2.log

service mediacenter stop
#sudo git pull
./install.sh
service mediacenter start
