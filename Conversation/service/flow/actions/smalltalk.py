from service.flow.states.statebase import StateBase

class smalltalk(StateBase):

    def handle(self, result):
        self.context.say(result.Text)

    def greetings(self, result):
        self.context.say(result.Text)