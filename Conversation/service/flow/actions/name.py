from service.flow.states.statebase import StateBase

class name(StateBase):

    def handle(self, result):
        self.context.log("trying to handle: " + str(result.ParsedJson))
        if(result is not None):
            if(result.Text is not None and len(result.Text) > 0):
                self.context.say(result.Text)
            else:
                self.context.show_notification(result.Text)
        else:
            self.unknown(result)

    def get(self, result):
        self.context.say("Hell I don't know")