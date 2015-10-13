#!/bin/bash
serviceFolder="/Applications/Kodi.app/Contents/Resources/Kodi/addons/service.oldphone.conversation"
programFolder="/Applications/Kodi.app/Contents/Resources/Kodi/addons/script.module.oldphone.conversation"
username="macbook"

if [ ! -d $serviceFolder ]
    then
        echo "creating $serviceFolder"
        mkdir $serviceFolder
fi

if [ ! -d $programFolder ]
    then
        echo "creating $programFolder"
        mkdir $programFolder
fi


cp -v -R ../program/* $programFolder/
cp -v -R ../service/* $serviceFolder/

if [ ! -f $programFolder/conversation.config ] || [ "$1" == "f" ]
    then
        echo "copying config"
        cp -v ./conversation.config $programFolder/conversation.config
fi

sudo chown -R $username $serviceFolder
sudo chown -R $username $programFolder

echo "Done"