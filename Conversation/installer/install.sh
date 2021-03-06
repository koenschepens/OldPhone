#!/bin/bash
serviceFolder="/home/osmc/.kodi/addons/service.oldphone.conversation"

if [ ! -d $serviceFolder ]
	then
		echo "creating $serviceFolder"
		mkdir $serviceFolder
fi

cp ../service/* $serviceFolder/ -v -R

if [ ! -f $serviceFolder/conversation.config ] || [ "$1" == "-f" ]
	then
		echo "copying config"
		cp ../service/conversation.config $serviceFolder/conversation.config -v
fi

sudo chown osmc $serviceFolder -R

sudo chmod 775 $serviceFolder -R

echo "Done"