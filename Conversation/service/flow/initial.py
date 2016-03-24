import sys

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