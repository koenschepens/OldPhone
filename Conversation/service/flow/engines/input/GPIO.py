__author__ = 'macbook'

import GPIO.GPIO as gpio

class GPIO():
    def __init__(self, context):
        gpio.setmode(gpio.BCM)
        gpio.setup(context.Config["gpio"]["hoorn"], gpio.IN, pull_up_down = gpio.PUD_DOWN)

    def input(self, channel):
        value = raw_input(("Int value for {0}: ").format(channel))
    
        while (not is_number(value)):
            print ("FOUT!")
            value = raw_input(("Int value for {0}: ").format(channel))
    
        return int(value)
        
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False
