import state
import contexts
import initial
import phoneDown
import actions

class PhoneUp(state.State):
    def go(self):
        while(self.Context.isUp()):
            whatyousaid = self.Context.getVoiceInput()

            self.Context.log(whatyousaid)
            result = self.Context.Conversation.ask(whatyousaid)

            self.Context.State = actions.actionState(self.Context)
            self.Context.State.handle(result)

        self.Context.State = phoneDown.PhoneDown(self.Context)
        self.Context.State.go()


        

