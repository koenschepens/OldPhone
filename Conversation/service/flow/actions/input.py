from service.flow.states.statebase import StateBase

class input(StateBase):

    def handle(self, result):
        self.context.log("trying to handle: " + str(result.ParsedJson))
        if(result is not None):
            if(result.Text is not None and len(result.Text) > 0):
                self.context.say(result.Text)
            else:
                self.context.show_notification(result.Text)
        else:
            self.unknown(result)

    def unknown(self, result):
        self.context.log("No understand: "+ str(result.ResolvedQuery))
        self.context.say("Sorry what?")