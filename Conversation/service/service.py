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
    dialog = xbmcgui.Dialog()
    dialog.notification('WHAT DO YOU WANT??!?!1', 'Example: play movie.', xbmcgui.NOTIFICATION_INFO, 5000)

    whatyousaid = executeScript('speech-recog.sh')
    xbmc.executebuiltin( "ActivateWindow(busydialog)" )

    whatyoushouldhavesaid = whatyousaid.strip('"')

    c = conversation.Conversation()
    result = c.ask(whatyoushouldhavesaid)

    whatwethinkyouwant = result.getKodiAction()
    
    xbmc.log(msg="response: " + whatwethinkyouwant.encode('utf8'), level=xbmc.LOGDEBUG)
    xbmcResult = xbmc.executeJSONRPC(whatwethinkyouwant.encode('utf8'))

    while(result.NextFunction is not None):
        print ("starting NextFunction" + str(result.NextFunction))
        if(result.NeedsUserInput):
            subprocess.call([ttsEngine, "Which movie you want yes?"])
            userInput = executeScript('speech-recog.sh')
            xbmcInput = json.loads(xbmcResult, object_pairs_hook=OrderedDict)['result']
            chosenItem = getChosenItem(userInput, xbmcInput)
            if(chosenItem is not None):
                nextFunctionResult = result.NextFunction(chosenItem)
            else:
                result.NextFunction = None
                nextFunctionResult = c.get_show_notification_json("Sorry","That movie is not in this list.", 300)
        else:
            print ("no user input required")
            nextFunctionResult = result.NextFunction(xbmcResult)
        
        xbmcResult = xbmc.executeJSONRPC(nextFunctionResult.replace(' ', '%20'))

    subprocess.call([ttsEngine, result.Text])

    xbmc.executebuiltin( "Dialog.Close(busydialog)" )


def getChosenItem(userInput, xbmcInput):
    if(len(xbmcInput) > 0):
        for key, value in xbmcInput.iteritems():
            if(xbmcInput[key] == userInput):
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