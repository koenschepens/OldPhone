from time import sleep
import RPi.GPIO as GPIO
from subprocess import call
import time
import os
from datetime import datetime
import sys
import logging
import ConfigParser
import traceback
import xbmcgui
import xbmcplugin
import xbmc, xbmcgui, xbmcaddon

def picked_up(argument):
    #call(["/home/osmc/Pi/PiAUISuite/ReadSpeaker/sayhello"])
    xbmc.log(msg='pickup!!!', level=xbmc.LOGDEBUG)
    result = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Addons.ExecuteAddon", "id": "script.module.oldphone.conversation"}')
    xbmc.log(msg=result, level=xbmc.LOGDEBUG)


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