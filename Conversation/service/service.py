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
folder = os.path.dirname(os.path.realpath(__file__))

config = ConfigParser.RawConfigParser()
configFile = os.path.join(folder, 'conversation.config')
config.read(configFile)

includesDir = os.path.dirname(os.path.realpath(__file__)) + '/includes/'
ttsEngine = config.get('settings', 'tts.engine').replace('$includesDir', includesDir)
language = 'dutch'

def picked_up(argument):
    xbmc.log(msg='using ' + ttsEngine + ' as ttsEngine', level=xbmc.LOGDEBUG)
    dialog = xbmcgui.Dialog()
    dialog.notification('Yes hello this is dog.', 'Speak..', xbmcgui.NOTIFICATION_INFO, 1000)

    whatyousaid = executeScript('speech-recog.sh').strip('"')
    #xbmc.executebuiltin( "ActivateWindow(busydialog)" )

    whatyoushouldhavesaid = whatyousaid.strip('"')

    c = conversation.Conversation()
    result = c.ask(whatyoushouldhavesaid)

    whatwethinkyouwant = result.getKodiAction()
    
    xbmc.log(msg="response: " + whatwethinkyouwant.encode('utf8'), level=xbmc.LOGDEBUG)
    xbmcResult = xbmc.executeJSONRPC(whatwethinkyouwant.encode('utf8'))

    while(result.NextFunction is not None):
        xbmc.log(msg="starting NextFunction: " + str(result.NextFunction), level=xbmc.LOGDEBUG)
        if(result.NeedsUserInput):
            subprocess.call([ttsEngine, "Which movie you want yes?"])
            userInput = executeScript('speech-recog.sh')
            xbmcInput = json.loads(xbmcResult)['result']
            chosenItem = getChosenItem(userInput, xbmcInput)
            if(chosenItem is not None):
                nextFunctionResult = result.NextFunction(chosenItem)
            else:
                result.NextFunction = None
                nextFunctionResult = c.get_show_notification_json("Sorry","The movie " + userInput + " is not in this list.", 300)
        else:
            xbmc.log(msg="no user input required", level=xbmc.LOGDEBUG)
            nextFunctionResult = result.NextFunction(xbmcResult)
        
        xbmcResult = xbmc.executeJSONRPC(nextFunctionResult.replace(' ', '%20'))

    subprocess.call([ttsEngine, result.Text])

    #xbmc.executebuiltin( "Dialog.Close(busydialog)" )


def getChosenItem(userInput, xbmcInput):
    if(len(xbmcInput) > 0):
        for key, value in xbmcInput.iteritems():
            if(xbmcInput[key].lower() == userInput.lower()):
                return { "Label" : xbmcInput[key], "FolderPath" : xbmcInput[key.replace(".Label", ".FolderPath")] }
    return None

def executeScript(script):
    script = includesDir + script
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