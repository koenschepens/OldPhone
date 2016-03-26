from service.flow.states.statebase import StateBase

__author__ = 'macbook'
class wisdom(StateBase):
    def unknown(self, result):
        self.context.say(result.Text)

    def handle(self, result):
        self.context.say(result.Text)

    def greetings(self, result):
        self.context.say(result.Text)