from service.flow.states.statebase import StateBase

class userInput(StateBase):

    def handle(self, result):
        choice = self.context.get_voice_input(question="Make a choice", ringBackTone = False, pling = True)
        self.context.log("user input: " + choice)
        return choice


