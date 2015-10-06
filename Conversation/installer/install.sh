#!/bin/bash

serviceFolder="/home/osmc/.kodi/addons/service.oldphone.conversation"
programFolder="/home/osmc/.kodi/addons/script.module.oldphone.conversation"

echo "installing program..."

echo "copying new files"
if [ ! -d $serviceFolder ]
	then
		echo "creating $serviceFolder"
		mkdir $serviceFolder
		sudo chown osmc $serviceFolder -R
fi

echo "copying program files"
cp ../program/* $serviceFolder/ -v -R

if [ ! -f $serviceFolder/conversation.config ] || [ "$1" == "f" ]
	then
		echo "copying config"
		cp ./conversation.config $serviceFolder/conversation.config -v
fi

echo "Installing service..."

echo "copying new files"
if [ ! -d $programFolder ]
	then
		echo "creating $serviceFolder"
		mkdir $programFolder
		sudo chown osmc $programFolder -R
fi

echo "Done"