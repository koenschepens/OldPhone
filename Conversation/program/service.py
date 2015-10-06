from time import sleep
import RPi.GPIO as GPIO
from subprocess import call
import time
from datetime import datetime
import sys
import logging
import ConfigParser

import xbmcgui
import xbmcplugin
import xbmc, xbmcgui, xbmcaddon

def picked_up(argument):
    main()
    call(["/home/osmc/Pi/PiAUISuite/ReadSpeaker/sayhello"])


GPIO.setmode(GPIO.BCM)
GPIO.setup(hoorn, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
new = True

while True:
    try:
        if(GPIO.input(hoorn) == 1):
            print("wait until hanging up...")
            picked_up(1)
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