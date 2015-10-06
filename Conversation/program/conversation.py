from time import sleep
import RPi.GPIO as GPIO
from enum import Enum
from subprocess import call
import time
from datetime import datetime
import sys
import logging
import ConfigParser
import sys
import xbmcgui
import xbmcplugin

try:
    from xbmc.xbmcclient import XBMCClient
except:
    sys.path.append('/usr/share/pyshared/xbmc')
    from xbmcclient import XBMCClient

addonFolder = "/home/osmc/.kodi/addons/service.conversation/" 

logging.basicConfig(filename=addonFolder + 'conversation.log',level=logging.INFO)
#logging.basicConfig(level=logging.INFO)

config = ConfigParser.RawConfigParser()
configFile = addonFolder + 'conversation.config'
logging.info("reading config file " + configFile)
config.read(configFile)

hoorn = 11
#buzzer = 26
	
#v = pyvona.create_voice("GDNAIRN4SS66PRNKPQZQ","2gURBTiaqnkjxEXZX+cslGhkJ+OVKTzWCZg7mvpp")
#v.speak("Hello! How nice of you to drop by.")

#GPIO.setup(buzzer, GPIO.OUT)
GPIO.setmode(GPIO.BCM)
GPIO.setup(hoorn, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
new=True

def picked_up(argument):
    logging.info(str(argument))
    call(["/home/osmc/Pi/PiAUISuite/ReadSpeaker/sayhello"])
    showMainWindow()

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

GPIO.add_event_detect(hoorn, GPIO.RISING, callback=picked_up) 

logging.info("Setting up Kodi client")

host = config.get("xbmc", "host")
port = config.getint("xbmc", "port")

logging.info("host: " + str(host))
logging.info("port: " + str(port))

# Create an XBMCClient object and connect (needed because we don't run as the same user as Kodi)
xbmc = XBMCClient("OldPhone", addonFolder + "icon.png")
xbmc.connect()

while True:
    try:
        sleep(0.02)
    except KeyboardInterrupt:
        logging.info("Exiting...")
        raise
    except:
        GPIO.cleanup()
        xbmc.close()
        logging.error("Unexpected error:", sys.exc_info()[0])
        logging.error("Unexpected error:", sys.exc_info()[1])
        raise
pass

