import flow.state
import flow.contexts

import conversation
from actionState import actionState

class configAction(actionState):

    def handle(self, result):
        immediateActions = self.Context.Config.options("immediateActions")

        if(result.Request in immediateActions):
            configValue = config.get("immediateActions", self.Request)

            self.Context.send_action(configValue)

   