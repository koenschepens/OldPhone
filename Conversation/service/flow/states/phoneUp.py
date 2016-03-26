from service.flow.actions.actionState import actionState
import statebase
import phoneDown

class PhoneUp(statebase.StateBase):
    def go(self):
        while(self.context.isUp()):
            result = self.context.ask()

            self.context.state = actionState(self.context)
            self.context.state.handle(result)

        self.context.state = phoneDown.PhoneDown(self.context)
        self.context.state.go()


        

