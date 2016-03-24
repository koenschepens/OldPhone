#!/bin/sh

#now=$(date +"%m_%d_%Y_%T")
#echo "********* update.sh **********" >> ~/keypadUpdater2.log

service mediacenter stop
#sudo git pull
./install.sh -f
service mediacenter start
#xbmc-send -a "RunPlugin(plugin://service.oldphone.conversation/)"
