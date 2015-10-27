import resources.lib.flow.states.abstract_state
import resources.lib.flow.contexts
import datetime

import resources.lib.conversation
from actionState import actionState

import time

class clock(actionState):

    def time(self, result):
        timestring = time.strftime("%H:%M")
        if("location" in result.Parameters):
            response = "I don't know the time in " + result.Parameters["location"] + ". The time here is: " + timestring
            self.Context.show_notification(response)
            self.Context.say(response)
        else:
            response = "The current time is " + timestring
            self.Context.show_notification(response)
            self.Context.say(response)
        
        return None