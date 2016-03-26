import statebase
import Conversation.service.flow.engines
import phoneDown
import Conversation.service.flow.actions

class PhoneUp(statebase.StateBase):
    def go(self):
        while(self.context.isUp()):
            result = self.context.ask()

            self.context.state = Conversation.service.flow.actions.actionState(self.context)
            self.context.state.handle(result)

        self.context.state = phoneDown.PhoneDown(self.context)
        self.context.state.go()


        

