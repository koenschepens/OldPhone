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
reload(sys) 
sys.setdefaultencoding('UTF8')

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

    xbmcResult = urllib2.urlopen('http://192.168.1.116/jsonrpc?request=' + kodiJson.replace(' ', '%20')).read()

    while(result.NextFunction is not None):
        print ("starting NextFunction" + str(result.NextFunction))
        if(result.NeedsUserInput):
            print ("NeedsUserInput")
            userInput = "pixels"
            xbmcInput = json.loads(xbmcResult)['result']
            chosenItem = getChosenItem(userInput, xbmcInput)
            if(chosenItem is not None):
                nextFunctionResult = result.NextFunction(chosenItem)
            else:
                result.NextFunction = None
                nextFunctionResult = c.get_show_notification_json("Sorry","The movie " + userInput + " is not in this list.", 300)
        else:
            print ("no user input required")
            nextFunctionResult = result.NextFunction(xbmcResult)
        
        xbmcResult = urllib2.urlopen('http://192.168.1.116/jsonrpc?request=' + nextFunctionResult.replace(' ', '%20')).read()
        print xbmcResult
    
    #subprocess.call([ttsEngine, result.Text])


def getChosenItem(userInput, xbmcInput):
    if(len(xbmcInput) > 0):
        for key, value in xbmcInput.iteritems():
            if(xbmcInput[key].lower() == userInput.lower()):
                return { "Label" : xbmcInput[key], "FolderPath" : xbmcInput[key.replace(".Label", ".FolderPath")] }
    return None

def executeScript(script):
    script = includesDir + script
    p = subprocess.Popen(script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out

hoorn = 11

new = True
picked_up(sys.argv[1])