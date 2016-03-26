from service.flow.states.statebase import StateBase

class news(StateBase):

    def handle(self, result):
        self.context.log(str(result.Parameters))

