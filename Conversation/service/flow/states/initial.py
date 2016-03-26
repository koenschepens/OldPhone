import sys

import statebase
import phoneDown
import phoneUp

reload(sys) 
sys.setdefaultencoding('UTF8')

class Initial(statebase.StateBase):
    def __init__(self, context):
        self.context = context

    def go(self):
        if(self.context.isUp()):
            self.context.State = phoneUp.PhoneUp(self.context)
        else:
            self.context.State = phoneDown.PhoneDown(self.context)
        
        self.context.State.go()