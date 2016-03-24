import flow.state
import flow.contexts

import conversation
from actionState import actionState

class message(actionState):

    def handle(self, result):
        self.Context.log(str(result.Parameters))

    def show(self, result):
        self.Context.log("message: "+str(result.Text))

