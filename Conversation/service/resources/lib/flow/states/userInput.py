import resources.lib.flow.states.abstract_state
import resources.lib.flow.contexts

import resources.lib.conversation
from actionState import actionState

class userInput(actionState):

    def handle(self, result):
        question = None
        if(result is not None):
            question = result.Text
        choice = self.Context.getVoiceInput(question=question, ringBackTone = False, pling = True)
        self.Context.log("user input: " + choice)
        return choice

    def send_to_kodi_input(self, result):
        return self.Context.send_input_to_client(self.handle(result))


