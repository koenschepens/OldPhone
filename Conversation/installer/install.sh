#!/bin/bash

serviceFolder="/home/osmc/.kodi/addons/service.conversation"

echo "installing..."

echo "copying new files"
if [ ! -d $serviceFolder ]
	then
		echo "creating $serviceFolder"
		mkdir $serviceFolder
fi

echo "copying program files"
cp ../program/* $serviceFolder/ -v

if [ ! -f $serviceFolder/conversation.config ] || [ "$1" == "f" ]
	then
		echo "copying config"
		cp ./conversation.config $serviceFolder/conversation.config -v
fi

echo "Done"