from time import sleep
import RPi.GPIO as GPIO
from enum import Enum
from subprocess import call
import time
from datetime import datetime
import sys
import logging
import os
import ConfigParser
import threading

def trace(frame, event, arg):
    print("%s, %s:%d" % (event, frame.f_code.co_filename, frame.f_lineno))

run = True

try:
    import xbmc
    import xbmcaddon
    import xbmcgui

    inXbmc = True
except:
    inXbmc = False
try:
    from xbmc.xbmcclient import XBMCClient,ACTION_EXECBUILTIN,ACTION_BUTTON
except:
    sys.path.append('/usr/share/pyshared/xbmc')
    from xbmcclient import XBMCClient,ACTION_EXECBUILTIN,ACTION_BUTTON

xClient = XBMCClient("Phone buttons are enabled")
xClient.connect()

if(inXbmc):
    addon = xbmcaddon.Addon('service.oldphone.keypad')
    addonFolder = addon.getAddonInfo('path')
    xbmc.log("using folder: " + addonFolder)
    sys.path.append(os.path.realpath(os.path.join(addonFolder, '..', 'service.oldphone.conversation')))
    logging.basicConfig(filename=os.path.join(addonFolder, 'keypad.log'),level=logging.INFO)
    configFile = os.path.realpath(os.path.join(addonFolder, 'keypad.config'))
    logging.info("in XBMC. Using config file " + configFile)
else:
    folder = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.realpath(os.path.join(folder, '../..', 'Conversation', 'service')))

    logging.basicConfig(level=logging.INFO)
    configFile = os.path.realpath(os.path.join(folder, '../installer', 'keypad.config'))
    logging.info("Not in XBMC. Using config file " + configFile)

KEYPAD_MODE_READROWS = 0
KEYPAD_MODE_READCOLUMNS = 1

HOORN_UP = True
HOORN_DOWN = False

initial_state = True 

verbose = "-v" in sys.argv
test = "-t" in sys.argv

config = ConfigParser.RawConfigParser()
logging.info("reading config file " + configFile)
config.read(configFile)

hoorn = config.getint("gpiomapping", "hoorn")
gpiokeymappings = config.options("gpiokeymapping")

try:
    hoornWaitTime = config.getfloat("settings", "hoornWaitTime")
    logging.info("Sleep wait time: " + str(hoornWaitTime))
except:
    hoornWaitTime = 0.25
    logging.warning("Can't find sleep setting. Defaulted to " + str(hoornWaitTime))

try:
    keypadWaitTime = config.getfloat("settings", "keypadWaitTime")
    logging.info("Sleep wait time: " + str(keypadWaitTime))
except:
    keypadWaitTime = 0.25
    logging.warning("Can't find sleep setting. Defaulted to " + str(keypadWaitTime))

try:
    bounceTime = config.getfloat("settings", "bounceTime")
    logging.info("BounceTime: " + str(bounceTime))
except:
    bounceTime = 0.25
    logging.warning("Can't find bounceTime setting. Defaulted to " + str(bounceTime))

now = datetime.now().isoformat()

logging.info(str(now))

logging.info("Setting GPIO mode to BCM")
GPIO.setmode(GPIO.BCM)

#contains a dictionary of each row an array of columns for that row
rowsWithColumns = {}

#keep seperate array with columns to check if already set up
columns = []
keys = {}
i = 1
processing = False
actions = {}

lastPing = datetime.now()

def listenToRows():
    global run
    global keypadWaitTime
    while(run):
        global rowsWithColumns
        global lastPing
        global initial_state

        if((lastPing - datetime.now()).seconds == 50):
            xClient.ping()
            lastPing = datetime.now()

        for row in rowsWithColumns:
            rowinput = GPIO.input(row)
            if(verbose):
                logging.info("Row " + str(row) + ": " + str(rowinput))
            if(rowinput):
                row_changed(row)
        sleep(keypadWaitTime)
    logging.info("Stopped listening to rows...")

def listenToHoorn():
    global run
    global hoorn
    global HOORN_UP
    global HOORN_DOWN
    global hoorn_previous_state
    global initial_state

    while(run):
        # also listen to hoorn
        hoorn_state = GPIO.input(hoorn)

        if(not initial_state and hoorn_previous_state != hoorn_state):
            if(hoorn_state == HOORN_UP):
                if(inXbmc):
                    xbmc.log(msg="hoorn up", level=xbmc.LOGDEBUG)
                send_key("hoorn_up")
            else:
                if(inXbmc):
                    xbmc.log(msg="hoorn down", level=xbmc.LOGDEBUG)
                send_key("hoorn_down")
            hoorn_previous_state = hoorn_state
        else:
            initial_state = False

        sleep(hoornWaitTime)

    logging.info("Stopped listening to hook...")


def send_key(key):
    global bounceTime

    if(config.has_option('default', key)):
        if(config.get('default', key) is not None):
            action = config.get('default', key)
            if(verbose or test):
                logging.info("pressed " + key)
            if(not test):
                xClient.send_keyboard_button(button=action)
                sleep(bounceTime)
                xClient.release_button()
        else:
            logging.warning("key " + key + " is not mapped")
    else:
        logging.warning("No default config found (" + key + " was pressed)")

def setRowEvents(row, mode):
    global bounceTime
    global rowsWithColumns
    if(mode == KEYPAD_MODE_READROWS):
        # Set row to IN
        if(GPIO.gpio_function(row) == GPIO.IN):
            logging.warning("Pin " + str(row) + " already set to IN")

        GPIO.setup(row, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        #GPIO.add_event_detect(row, GPIO.RISING, callback=row_changed, bouncetime=bounceTime)
        
        # Set columns to OUT
        for column in rowsWithColumns[row]:
            if(GPIO.gpio_function(column) == GPIO.OUT):
                logging.warning("Pin " + str(column) + " already set to OUT")
            else:
                GPIO.setup(column, GPIO.OUT, initial=1)
    else:
        # Set row to OUT
        #GPIO.remove_event_detect(row)
        if(GPIO.gpio_function(row) == GPIO.OUT):
            logging.warning("Pin " + str(row) + " already set to OUT")
        else:
            GPIO.setup(row, GPIO.OUT, initial=1)
        
        # Set columns to IN
        for column in rowsWithColumns[row]:
            if(GPIO.gpio_function(column) == GPIO.IN):
                logging.warning("Pin " + str(column) + " already set to IN")
            
            GPIO.setup(column, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #sleep(0.02)

def row_changed(row):
    if(verbose):
        logging.info("Row " + str(row) + " has changed")
    global processing
    global rowsWithColumns
    global columns
    global keys

    if(not processing):
        processing = True
        # Disable events until action is done
        setRowEvents(row, KEYPAD_MODE_READCOLUMNS)

        # Read which column it was
        for column in rowsWithColumns[row]:
            columnValue = GPIO.input(column)

            if(columnValue):
                key = keys[str(row) + "," + str(column)]
                send_key(key)                
                pass

        # Re-enable events
        setRowEvents(row, KEYPAD_MODE_READROWS)
        sleep(0.1)

        #GPIO.wait_for_edge(row, GPIO.FALLING)

        processing = False
    else:
        logging.info("already processing, ignored")

# Read all GPIO key mappings and add them to the keys dictionary 
for option in gpiokeymappings:
    row = int(config.get("gpiokeymapping", option).split(",")[0])
    column = int(config.get("gpiokeymapping", option).split(",")[1])

    # define key for later retrieval
    logging.info("adding " + option + " as " + str(row) + "," + str(column) + "")
    keys[config.get("gpiokeymapping", option)] = option

    if row not in rowsWithColumns:
        rowsWithColumns[row] = [column]
    else:
        rowsWithColumns[row].append(column)

    if column not in columns:
        columns.append(column)

for row in rowsWithColumns:
    setRowEvents(row, KEYPAD_MODE_READROWS)


GPIO.setup(hoorn, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
hoorn_previous_state = GPIO.input(hoorn)

#GPIO.add_event_detect(hoorn, GPIO.BOTH, callback=phonePickedUp)

threadRows = threading.Thread(target=listenToRows)
threadHoorn = threading.Thread(target=listenToHoorn)

threadRows.start()
threadHoorn.start()

def cleanup():
    logging.info("Stopping threads...")
    global run
    run = False
    logging.info("Cleaning up GPIO...")
    GPIO.cleanup()


if(inXbmc):
    logging.info("using xbmc context")
    if __name__ == '__main__':
        logging.info("main")
        monitor = xbmc.Monitor()
     
        logging.info("abortRequested=" + str(monitor.abortRequested()))
        logging.info("will be listening to: " + str(rowsWithColumns))
        while not monitor.abortRequested():
            if monitor.waitForAbort(0.5):
                cleanup()
                break
else:
    try:
        while(True):
            sleep(0.5)
    except:
        cleanup()
        raise



