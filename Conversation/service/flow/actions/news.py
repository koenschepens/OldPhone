import flow.state
import flow.contexts

import conversation
from actionState import actionState

class news(actionState):

    def handle(self, result):
        self.Context.log(str(result.Parameters))

    def search(self, result):
        self.Context.log("news: "+str(result.Parameters))