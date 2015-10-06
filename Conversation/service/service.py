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
import xbmc, xbmcgui, xbmcaddon

def picked_up(argument):
    #call(["/home/osmc/Pi/PiAUISuite/ReadSpeaker/sayhello"])
    xbmc.log(msg='pickup!!!', level=xbmc.LOGDEBUG)
    #executeAddon("plugin.video.youtube", '"url": "https://www.youtube.com/watch?v=f5RauCBguH0"')
    dialog = xbmcgui.Dialog()
    dialog.notification('Wat wil je doen?', 'Bijv: Youtube.', xbmcgui.NOTIFICATION_INFO, 5000)

    whatyousaid = executeScript('/home/osmc/.kodi/addons/service.oldphone.conversation/includes/speech-recog.sh', None)
    whatyoushouldhavesaid = whatyousaid.strip('"')
    
    xbmc.log(msg='you said ' + whatyoushouldhavesaid, level=xbmc.LOGDEBUG)

    whatyouwant = executeScript('/home/osmc/.kodi/addons/service.oldphone.conversation/includes/youtube-search', whatyoushouldhavesaid)
    playYoutubeVideo(whatyouwant)

def executeAddon(addonid, params):
    result = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Addons.ExecuteAddon", "params": { "wait": false, "addonid": "' + addonid + '", "params": { ' + params + ' } }, "id": 2 }')

    xbmc.log(msg=result, level=xbmc.LOGDEBUG)

def executeScript(script, arguments):
    if(arguments is None):
        p = subprocess.Popen([script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        p = subprocess.Popen([script, arguments], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out, err = p.communicate()
    return out

def playYoutubeVideo(youtubeId):
    result = xbmc.executeJSONRPC('{"id":1,"jsonrpc":"2.0","method":"Player.Open","params":{"item":{"file":"plugin:\/\/plugin.video.youtube\/?path=\/root\/search&action=play_video&videoid=' + youtubeId + '"}}}')
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