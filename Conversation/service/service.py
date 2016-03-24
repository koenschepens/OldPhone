from time import sleep

import sys
import os

try:
    import GPIO.GPIO as GPIO
except:
    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'includes', 'GPIO'))
    import GPIO as GPIO

import subprocess
import commands
import time
from datetime import datetime
import logging
import ConfigParser
import traceback
import xbmcgui
import xbmcplugin
import xbmc, xbmcaddon
import json

import conversation
folder = os.path.dirname(os.path.realpath(__file__))

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'kodi'))
import kodi_container

config = ConfigParser.RawConfigParser()
configFile = os.path.join(folder, 'conversation.config')
config.read(configFile)

includesDir = os.path.dirname(os.path.realpath(__file__)) + '/includes/'
ttsEngine = config.get('settings', 'tts.engine').replace('$includesDir', includesDir)
speechRecognitionEngine = includesDir + 'speech-recog.sh'
language = 'dutch'

def picked_up(argument):
    dialog = xbmcgui.Dialog()
    dialog.notification('Yes hello this is dog.', 'Speak..', xbmcgui.NOTIFICATION_INFO, 1000)

    whatyousaid = executeScript(speechRecognitionEngine).strip('"')
    #xbmc.executebuiltin( "ActivateWindow(busydialog)" )

    whatyoushouldhavesaid = whatyousaid.strip('"')

    c = conversation.Conversation()
    result = c.ask(whatyoushouldhavesaid)

    whatwethinkyouwant = result.getKodiAction()

    xbmc.log(msg="speechRecognitionEngine: " + speechRecognitionEngine, level=xbmc.LOGDEBUG)
    xbmc.log(msg="ttsEngine: " + ttsEngine, level=xbmc.LOGDEBUG)
    
    xbmc.log(msg="response: " + whatwethinkyouwant.encode('utf8'), level=xbmc.LOGDEBUG)
    xbmcResult = xbmc.executeJSONRPC(whatwethinkyouwant.encode('utf8'))

    # Get current screen and list
    container = kodi_container.Container()
    container.load()

    xbmc.log(msg = "container dir: " + str(dir(container)))

    if(container.hasItems()):
        container.updateItems()
        subprocess.call([ttsEngine, "Which one?"])
        userInput = executeScript(speechRecognitionEngine).strip('"')
        xbmc.log(msg = "getting label: " + userInput)
        item = container.getItemByLabel(userInput)
        if(item is not None):
            item.play()

    #subprocess.call([ttsEngine, result.Text])

    #xbmc.executebuiltin( "Dialog.Close(busydialog)" )

def executeScript(script):
    print(script)
    p = subprocess.Popen(script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out

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