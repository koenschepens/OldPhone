from time import sleep
import RPi.GPIO as GPIO
import subprocess 
import commands
import time
import os
from datetime import datetime
import sys
import logging
import ConfigParser
import traceback
import xbmcgui
import xbmcplugin
import xbmc, xbmcaddon
import json

import conversation

tokens = { 'dutch' : 'b240ec13475a464890af46b48f49f5c7', 'english' : 'fb928615eb914f4785e110eecad49c95' }

language = sys.argv[1]

def picked_up(argument):
    c = conversation.Conversation(tokens[language], '7c4c06c1-eb1d-4fd3-9367-134f20cbcb25')
    #call(["/home/osmc/Pi/PiAUISuite/ReadSpeaker/sayhello"])
    xbmc.log(msg='pickup!!!', level=xbmc.LOGDEBUG)
    #executeAddon("plugin.video.youtube", '"url": "https://www.youtube.com/watch?v=f5RauCBguH0"')
    dialog = xbmcgui.Dialog()
    dialog.notification('WHAT DO YOU WANT??!?!1', 'Example: play movie.', xbmcgui.NOTIFICATION_INFO, 5000)

    whatyousaid = executeScript('/home/osmc/.kodi/addons/service.oldphone.conversation/includes/speech-recog.sh')
    whatyoushouldhavesaid = whatyousaid.strip('"')

    xbmc.log(msg='you said ' + whatyoushouldhavesaid, level=xbmc.LOGDEBUG)
    
    xbmc.executebuiltin( "ActivateWindow(busydialog)" )
    c.ask(whatyoushouldhavesaid)
    xbmc.executebuiltin( "Dialog.Close(busydialog)" )

hoorn = 11

new = True

GPIO.setmode(GPIO.BCM)
GPIO.setup(hoorn, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

sleep(4)

while True:
    try:
        if(GPIO.input(hoorn) == 1):
            xbmc.log(msg='wait until hanging up...', level=xbmc.LOGDEBUG)
            picked_up(1)
            while(GPIO.input(hoorn) == 1):
                #call(["/home/osmc/Pi/PiAUISuite/ReadSpeaker/anythingelse"])
                #voicecommand = subprocess.Popen(["/home/osmc/Pi/PiAUISuite/VoiceCommand/voicecommand", "-c", "-f", "/home/osmc/$
                #runningPid = voicecommand.pid;
                time.sleep(0.25)
        if(GPIO.input(hoorn) == 0):
            os.system('pkill voicecommand')
            if(new):
                xbmc.log(msg='Phone is down', level=xbmc.LOGDEBUG)
                new=False
            else:
                xbmc.log(msg='Hung up', level=xbmc.LOGDEBUG)
            while (GPIO.input(hoorn) == 0):
                #wait until someone picks up the phone
                time.sleep(1)
    except KeyboardInterrupt:
        xbmc.log(msg='bye', level=xbmc.LOGERROR)
        raise
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        
        GPIO.cleanup()
        xbmc.log(msg=''.join('!! ' + line for line in lines), level=xbmc.LOGERROR)
        raise