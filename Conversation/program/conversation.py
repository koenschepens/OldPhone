from time import sleep
import RPi.GPIO as GPIO
from enum import Enum
from subprocess import call
import time
from datetime import datetime
import sys
import logging
import ConfigParser
sys.path.append('/usr/share/pyshared/xbmc')

from xbmcclient import XBMCClient
import xbmcgui
import xbmcplugin
import xbmc, xbmcgui, xbmcaddon


ADDON = xbmcaddon.Addon(id='scripts.module.oldphone.conversation')

addonFolder = "/home/osmc/.kodi/addons/scripts.module.oldphone.conversation/" 

logging.basicConfig(filename=addonFolder + 'conversation.log',level=logging.INFO)
#logging.basicConfig(level=logging.INFO)

config = ConfigParser.RawConfigParser()
configFile = addonFolder + 'conversation.config'
logging.info("reading config file " + configFile)
config.read(configFile)

hoorn = 11
##buzzer = 26
	
##v = pyvona.create_voice("GDNAIRN4SS66PRNKPQZQ","2gURBTiaqnkjxEXZX+cslGhkJ+OVKTzWCZg7mvpp")
##v.speak("Hello! How nice of you to drop by.")

##GPIO.setup(buzzer, GPIO.OUT)

GPIO.setmode(GPIO.BCM)
GPIO.setup(hoorn, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

new=True

def picked_up(argument):
    main()
    call(["/home/osmc/Pi/PiAUISuite/ReadSpeaker/sayhello"])

def showMainWindow():
    addon_handle = int(sys.argv[1])

    xbmcplugin.setContent(addon_handle, 'movies')

    url = 'http://download.wavetlan.com/SVV/Media/HTTP/mkv/H264_PCM(mkvmerge).mkv'
    li = xbmcgui.ListItem('A video!', iconImage='DefaultVideo.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)

def startVoiceCommand():
	os.system('pkill voicecommand')
	voicecommand = subprocess.Popen(["/home/osmc/Pi/PiAUISuite/VoiceCommand/voicecommand", "-c",  "-f", "/home/osmc/Pi/PiAUISuite/VoiceCommand/.commands.conf"])
	runningPid = voicecommand.pid;

#class Window(WindowXMLDialog):    
class main():
    def __init__(self):
        arg = self.getArg()
        if arg == 'INFO':
            self.showInfo()
        elif arg == 'UPDATE':
            self.update()
        else:
            self.showWelcome()

    def getArg(self):
        return sys.argv[-1]

    def _update(self):
        xbmcgui.Dialog().ok('Not supported')

    def showInfo(self,updated=False):
        xbmcgui.Dialog().ok('Conversation','by Koen Schepens','okdoei')

    def showWelcome(main=None):
        w = OptionsDialog('welcome.xml',ADDON.getAddonInfo('path'),'main','720p',main=main)
        w.setupButtons(10, 29, 300, 30)
        w.doModal()
        del w

    def showThingy(self):
        xbmcgui.Dialog().ok('Conversation','by Koen Schepens','okdoei')


GPIO.setmode(GPIO.BCM)
GPIO.setup(hoorn, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
new = True

while True:
    try:
        if(GPIO.input(hoorn) == 1):
            print("wait until hanging up...")
            main()
            while(GPIO.input(hoorn) == 1):
                    #call(["/home/osmc/Pi/PiAUISuite/ReadSpeaker/anythingelse"])
                    #voicecommand = subprocess.Popen(["/home/osmc/Pi/PiAUISuite/VoiceCommand/voicecommand", "-c", "-f", "/home/osmc/$
                    #runningPid = voicecommand.pid;
                    time.sleep(1)
        if(GPIO.input(hoorn) == 0):
            os.system('pkill voicecommand')
            if(new):
                    print("Phone is down")
                    new=False
            else:
                    print("Hung up")
            while (GPIO.input(hoorn) == 0):
                    #wait until someone picks up the phone
                    time.sleep(1)
    except KeyboardInterrupt:
        print("Bye... Cleaning up...")
        raise
    except:
        GPIO.cleanup()


