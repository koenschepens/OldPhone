import flow.state
import flow.contexts

import conversation
from actionState import actionState

class images(actionState):

    def search(self, result):
        self.Context.log("image search: "+str(result.ParsedJson))
