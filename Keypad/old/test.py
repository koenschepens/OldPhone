from time import sleep
import GPIO.GPIO as GPIO
from enum import Enum
from subprocess import call
import time
from datetime import datetime
import sys
import logging

class G(Enum):
    NONE = 0
    BCM08 = 1
    BCM07 = 2
    BCM05 = 4
    BCM06 = 8
    BCM12 = 16
    BCM13 = 32
    BCM19 = 64
    BCM16 = 128
    BCM26 = 256
    BCM20 = 512
    BCM21 = 1024
   
    BUTTON1 = BCM19+BCM20
    BUTTON2 = BCM19+BCM26
    BUTTON3 = BCM19+BCM16
    BUTTON4 = BCM13+BCM20
    BUTTON5 = BCM13+BCM26
    BUTTON6 = BCM13+BCM16
    BUTTON7 = BCM12+BCM20
    BUTTON8 = BCM05+BCM12
    BUTTON9 = BCM12+BCM16
    BUTTON0 = BCM21+BCM06
    BUTTONSTER = BCM06+BCM20
    BUTTONHEK = BCM08+BCM07


#logging.basicConfig(filename=addonFolder + 'keypad.log',level=logging.INFO)
logging.basicConfig(level=logging.INFO)

now = datetime.now().isoformat()

logging.info(str(now))

#logging.info("Cleanup GPIO")
#GPIO.cleanup()
logging.info("Setting GPIO mode to BCM")
GPIO.setmode(GPIO.BCM)

def setReadWrite(channelsToDown, channelsToUp):
    logging.info("switching rows/columns")
    for row in channelsToDown:
        #logging.info("Setting up channel " + str(row) + " to PUD_DOWN. ")
        GPIO.setup(row, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    for column in channelsToUp:
        #logging.info("Setting up channel " + str(column) + " to PUD_UP. ")
        #GPIO.setup(column, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(column, GPIO.OUT)



rows = [7,6,12,13,19]
columns = [21,8,5,16,26,20]
channelEnums = [G.BCM07,G.BCM06,G.BCM12,G.BCM13,G.BCM19,G.BCM21,G.BCM08,G.BCM05,G.BCM16,G.BCM26,G.BCM20]
values = [0,0,0,0,0,0,0,0,0,0]
i = 1

while True:

    #switch columns to input to read the values
    setReadWrite(columns, rows)

    for column in columns:
        value = GPIO.input(column)
        logging.info("column " + str(column) + " in mode " + str(GPIO.getmode(column)) + ": " + str(value))


    #switch back to reading rows  
    setReadWrite(rows, columns)
    for row in rows:
        value = GPIO.input(row)
        logging.info("row " + str(row) + " in mode " + str(GPIO.getmode(row)) + ": " + str(value))

    sleep(1)

    logging.info("." * i)
    i = i + 1    
