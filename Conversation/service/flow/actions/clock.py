from service.flow.states.statebase import StateBase

import time

class clock(StateBase):

    def time(self, result):
        timestring = time.strftime("%H:%M")
        if("location" in result.Parameters):
            response = "I don't know the time in " + result.Parameters["location"] + ". The time here is: " + timestring
            self.context.show_notification(response)
            self.context.say(response)
        else:
            response = "The current time is " + timestring
            self.context.show_notification(response)
            self.context.say(response)
        
