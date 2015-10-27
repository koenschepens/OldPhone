import resources.lib.flow
from resources.lib.flow.states import configActionState
from resources.lib.flow.states import abstract_state
import resources.lib.flow.states 
from resources.lib.flow.contexts import *
import resources.lib.conversation
import sys

class actionState(abstract_state.State):

    def handle(self, result):
        immediateActions = self.Context.Config.options("immediateActions")

        if(isinstance(result, basestring)):
            self.Context.State = resources.lib.flow.states.configActionState(self.Context)
            self.Context.State.handle(result)
            return

        configState = configActionState.configActionState(self.Context)

        if(not configState.handle(result)):
            self.Context.log("Not a config action: " + str(result.Action))

            actionItems = result.Action.split('.')

            try:
                mod = __import__('resources.lib.flow.states.' + actionItems[0], fromlist=[actionItems[0]])
                self.Context.State = getattr(mod, actionItems[0])(self.Context)
                self.Context.log("domain " + actionItems[0] + " exists. ")
            except ImportError:
                self.Context.State = resources.lib.flow.states.configActionState.configActionState(self.Context)
                self.Context.log("domain " + actionItems[0] + " does not exist. Using config")
            
            if(hasattr(self.Context.State, actionItems[1])):
                self.Context.log("actionState action: " + actionItems[1])
                action = getattr(self.Context.State, actionItems[1])
                return action(result)
            else:
                self.Context.log("action does not exist: " + actionItems[1] + ". Using " + self.Context.State.__class__.__name__ + ".handle()")
                return self.Context.State.handle(result)

        # Check if user input is required
        if(self.Context.userInputRequired()):
            import resources.lib.flow.states.input as Input
            self.Context.State = Input.input(self.Context)
            return self.Context.State.handle(result)
        

