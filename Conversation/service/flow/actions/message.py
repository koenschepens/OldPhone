from Conversation.service.flow.states.statebase import StateBase

class message(StateBase):

    def handle(self, result):
        self.context.log(str(result.Parameters))

    def show(self, result):
        self.context.log("message: "+str(result.Text))

