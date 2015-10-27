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

import abstract_state
import phoneDown
import phoneUp

reload(sys) 
sys.setdefaultencoding('UTF8')

class Initial(abstract_state.State):
    def __init__(self, context):
        self.Context = context

    def handle(self, result):
        pass