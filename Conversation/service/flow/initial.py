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

import state
import phoneDown
import phoneUp

reload(sys) 
sys.setdefaultencoding('UTF8')

class Initial(state.State):
    def __init__(self, context):
        self.Context = context

    def go(self):
        if(self.Context.isUp()):
            self.Context.State = phoneUp.PhoneUp(self.Context)
        else:
            self.Context.State = phoneDown.PhoneDown(self.Context)
        
        self.Context.State.go()