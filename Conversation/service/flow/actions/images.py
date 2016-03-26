from service.flow.states.statebase import StateBase

class images(StateBase):

    def search(self, result):
        self.context.log("image search: "+str(result.ParsedJson))
