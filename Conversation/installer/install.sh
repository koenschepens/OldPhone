#!/bin/bash

serviceFolder="/home/osmc/.kodi/addons/service.oldphone.conversation"
programFolder="/home/osmc/.kodi/addons/script.module.oldphone.conversation"

if [ ! -d $serviceFolder ]
	then
		echo "creating $serviceFolder"
		mkdir $serviceFolder
		sudo chown osmc $serviceFolder -R
fi

if [ ! -d $programFolder ]
	then
		echo "creating $programFolder"
		mkdir $programFolder
		sudo chown osmc $programFolder -R
fi


cp ../program/* $programFolder/ -v -R
cp ../service/* $serviceFolder/ -v -R

if [ ! -f $programFolder/conversation.config ] || [ "$1" == "f" ]
	then
		echo "copying config"
		cp ./conversation.config $programFolder/conversation.config -v
fi

echo "Done"