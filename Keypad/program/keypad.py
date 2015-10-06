from time import sleep
import RPi.GPIO as GPIO
from enum import Enum
from subprocess import call
import time
from datetime import datetime
import sys
import logging
import ConfigParser

try:
    from xbmc.xbmcclient import XBMCClient,ACTION_EXECBUILTIN,ACTION_BUTTON
except:
    sys.path.append('/usr/share/pyshared/xbmc')
    from xbmcclient import XBMCClient,ACTION_EXECBUILTIN,ACTION_BUTTON

addonFolder = "/home/osmc/.kodi/addons/service.keypad/" 

logging.basicConfig(filename=addonFolder + 'keypad.log',level=logging.INFO)
#logging.basicConfig(level=logging.INFO)

hoorn = 11

config = ConfigParser.RawConfigParser()
configFile = addonFolder + 'keypad.config'
logging.info("reading config file " + configFile)
config.read(configFile)

now = datetime.now().isoformat()

logging.info(str(now))

logging.info("Setting GPIO mode to BCM")
GPIO.setmode(GPIO.BCM)

#contains a dictionary of each row an array of columns for that row
rows = {}

#keep seperate array with columns to check if already set up
columns = []
keys = {}
i = 1

def send_key(key):
    try:
        xbmc.send_keyboard_button(button=key)
        sleep(0.25)
        xbmc.release_button()
    except:
        logging.warning("value invalid")

def picked_up(horn):
    xbmc.send_action("RunAddon('script.module.oldphone.conversation')")

def row_changed(row):
    global rows
    GPIO.remove_event_detect(row)
    GPIO.setup(row, GPIO.OUT)

    for column in rows[row]:
        GPIO.setup(column, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # Send signal from row to columns
    GPIO.output(row, 1)
    #sleep(0.05)

    # Read which column it was
    for column in rows[row]:
        columnValue = GPIO.input(column)

        if(columnValue):
            key = keys[str(row) + "," + str(column)]
            logging.info("row changed: " + str(row))
            send_key(key)

    # Set row and columns back to original setup
    GPIO.setup(row, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    for column in rows[row]:
        GPIO.remove_event_detect(column)
        GPIO.setup(column, GPIO.OUT)
        GPIO.output(column, 1)

    GPIO.add_event_detect(row, GPIO.RISING, callback=row_changed) 

gpiokeymappings = config.options("gpiokeymapping")

# Read all GPIO key mappings and ad them to the keys dictionary 
for option in gpiokeymappings:
    row = int(config.get("gpiokeymapping", option).split(",")[0])
    column = int(config.get("gpiokeymapping", option).split(",")[1])

    # define key for later retrieval
    keys[config.get("gpiokeymapping", option)] = option
    logging.info("setting up " + option + " as " + str(row) + "," + str(column) + "")

    if row not in rows:
        rows[row] = [column]
        GPIO.setup(row, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(row, GPIO.RISING, callback=row_changed) 
    else:
        rows[row].append(column)

    if column not in columns:
        columns.append(column)
        GPIO.setup(column, GPIO.OUT)
        GPIO.output(column, 1)

logging.info("Setting up Kodi client")

host = config.get("xbmc", "host")
port = config.getint("xbmc", "port")

logging.info("host: " + str(host))
logging.info("port: " + str(port))

# Create an XBMCClient object and connect (needed because we don't run as the same user as Kodi)
xbmc = XBMCClient("OldPhone", addonFolder + "/icon.png")
xbmc.connect()

#GPIO.setup(hoorn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.add_event_detect(hoorn, GPIO.RISING, callback=picked_up) 
 
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