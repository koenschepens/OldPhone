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

import conversation

tokens = { 'dutch' : 'b240ec13475a464890af46b48f49f5c7', 'english' : 'fb928615eb914f4785e110eecad49c95' }
includesDir = os.path.dirname(os.path.realpath(__file__)) + '/includes/'
language = 'dutch'

def picked_up(argument):
    #call(["/home/osmc/Pi/PiAUISuite/ReadSpeaker/sayhello"])
    print('pickup!!!')
    #executeAddon("plugin.video.youtube", '"url": "https://www.youtube.com/watch?v=f5RauCBguH0"')
    
    print('WHAT DO YOU WANT??!?!1', 'Example: play movie.')

    whatyousaid = "youtube play kittens"
    whatyoushouldhavesaid = whatyousaid.strip('"')

    c = conversation.Conversation(tokens[language], '7c4c06c1-eb1d-4fd3-9367-134f20cbcb25')
    whatwethinkyouwant = c.ask(whatyousaid)
    
    print(whatwethinkyouwant)

def executeScript(script):
    script = includesDir + script
    print(script)
    p = subprocess.Popen(script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out

hoorn = 11

new = True
picked_up(sys.argv[1])