import flow.state
import flow.contexts

import conversation
from actionState import actionState

class userInput(actionState):

    def handle(self, result):
        choice = self.Context.getVoiceInput(question="Make a choice", ringBackTone = False, pling = True)
        self.Context.log("user input: " + choice)
        return choice


