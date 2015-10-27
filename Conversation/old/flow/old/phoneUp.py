import abstract_state
import contexts
import initial
import phoneDown
import states

class PhoneUp(abstract_state.State):
    def handle(self, result):
        while(self.Context.isUp()):
            whatyousaid = self.Context.getVoiceInput()

            self.Context.log(whatyousaid)
            result = resources.lib.flow.states.Context.Conversation.ask(whatyousaid)

            self.Context.State = resources.lib.flow.states.actionState(self.Context)
            self.Context.State.handle(result)

        self.Context.State = phoneDown.PhoneDown(self.Context)
        self.Context.State.handle(None)


        

