#!/bin/bash

serviceFolder="/home/osmc/.kodi/addons/service.oldphone.voiceinput"

echo "installing..."

echo "copying new files"
if [ ! -d $serviceFolder ]
    then
        echo "creating $serviceFolder"
        mkdir $serviceFolder
fi

echo "copying program files"
cp ../program/* $serviceFolder/ -v -R

if [ ! -f $serviceFolder/voiceinput.config ] || [ "$1" == "-f" ]
    then
        echo "copying config"
        cp ./voiceinput.config $serviceFolder/voiceinput.config -v
fi

sudo chown osmc $serviceFolder -R
sudo chmod 775 $serviceFolder -R

echo "Done"