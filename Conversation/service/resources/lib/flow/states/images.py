import resources.lib.flow.states.abstract_state
import resources.lib.flow.contexts

import resources.lib.conversation
from actionState import actionState

class images(actionState):

    def search(self, result):
        self.Context.log("image search: "+str(result.ParsedJson))
