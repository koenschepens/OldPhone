from time import sleep
import subprocess 
import commands
import time
import os
from datetime import datetime
import sys
import logging
import ConfigParser
import traceback
import json
import urllib2


import conversation



try:
    from xbmc.xbmcclient import XBMCClient
except:
    sys.path.append('/Library/XbmcLib/')
    from xbmcclient import XBMCClient

folder = os.path.dirname(os.path.realpath(__file__))

config = ConfigParser.RawConfigParser()
configFile = os.path.join(folder, 'conversation.config')
config.read(configFile)

ttsEngine = config.get('settings', 'tts.engine')

includesDir = os.path.dirname(os.path.realpath(__file__)) + '/includes/'

def picked_up(argument):
    global x

    whatyousaid = argument
    whatyoushouldhavesaid = whatyousaid.strip('"')

    c = conversation.Conversation()
    result = c.ask(whatyousaid)
    kodiJson = result.getKodiAction()
    
    print(kodiJson)
    urllib2.urlopen('http://192.168.1.116/jsonrpc?request=' + kodiJson.replace(' ', '%20')).read()
    subprocess.call([ttsEngine, result.Text])

    print(result.getAudioStream())

def executeScript(script):
    script = includesDir + script
    print(script)
    p = subprocess.Popen(script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out

hoorn = 11

new = True
picked_up(sys.argv[1])