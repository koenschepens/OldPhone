import resources.lib.flow.states.abstract_state
import resources.lib.flow.contexts
import resources.lib.conversation
from actionState import actionState

class smalltalk(actionState):

    def handle(self, result):
        self.Context.show_notification(result.Text)

    def greetings(self, result):
        self.Context.say(result.Text)