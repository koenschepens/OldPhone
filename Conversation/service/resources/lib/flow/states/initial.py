import resources.lib.flow.states.abstract_state
import resources.lib.flow.contexts

import resources.lib.conversation
from actionState import actionState

class initial(actionState):

    def handle(self, result):
        self.Context.log("Getting user input...")
        whatyousaid = self.Context.getVoiceInput()
        self.Context.log("Done: " + whatyousaid)

        result = self.Context.Conversation.ask(whatyousaid)

        self.Context.State = actionState(self.Context)
        return self.Context.State.handle(result)