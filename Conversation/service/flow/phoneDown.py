import state
import contexts
import initial
import time
import phoneUp

class PhoneDown(state.State):
    def go(self):
        time.sleep(0.25)

        while (not self.Context.isUp()):
            time.sleep(0.25)

        self.Context.State = phoneUp.PhoneUp(self.Context)
        self.Context.State.go()