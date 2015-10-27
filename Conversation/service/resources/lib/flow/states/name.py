import resources.lib.flow.states.abstract_state
import resources.lib.flow.contexts

import resources.lib.conversation
from actionState import actionState

class name(actionState):

    def handle(self, result):
        self.Context.log("trying to handle: " + str(result.ParsedJson))
        if(result is not None):
            if(result.Text is not None and len(result.Text) > 0):
                self.Context.say(result.Text)
            else:
                self.Context.show_notification(result.Text)
        else:
            self.unknown(result)

    def get(self, result):
        self.Context.say("Hell I don't know")