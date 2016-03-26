import time

import statebase
import phoneUp


class PhoneDown(statebase.StateBase):
    def go(self):
        time.sleep(0.25)

        while (not self.context.isUp()):
            time.sleep(0.25)

        self.context.State = phoneUp.PhoneUp(self.context)
        self.context.State.go()