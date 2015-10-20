import flow
from flow import state
from flow.actions import *
from flow.contexts import *
import conversation
import sys

class actionState(state.State):

    def handle(self, result):
        immediateActions = self.Context.Config.options("immediateActions")

        if(isinstance(result, basestring)):
            self.Context.State = flow.actions.configAction(self.Context)
            self.Context.State.handle(result)
            return

        #for item in dir(result):
        #    self.Context.log(str(getattr(result, item)))
        self.Context.log("Action: " + str(result.Action))

        actionList = result.Action.split('.')
        actionClassess = {
            "media": flow.actions.media,
            "smalltalk": flow.actions.smalltalk,
            "weather": flow.actions.weather,
            "news": flow.actions.news,
            "smalltalk": flow.actions.smalltalk,
            "input": flow.actions.input,
            "images": flow.actions.images,
            "message": flow.actions.message,
            "clock": flow.actions.clock
        }

        if(actionList[0] in actionClassess):
            self.Context.log("domain exists :" + actionList[0])
            self.Context.State = actionClassess[actionList[0]](self.Context)
        else:
            self.Context.log("domain " + actionList[0] + " does not exist. Using config")
            self.Context.State = flow.actions.input(self.Context)
        
        if(hasattr(self.Context.State, actionList[1])):
            self.Context.log("actionState action: " + actionList[1])
            action = getattr(self.Context.State, actionList[1])
            action(result)
        else:
            self.Context.log("action does not exist: " + actionList[1] + ". Using " + self.Context.State.__class__.__name__ + ".handle()")
            self.Context.State.handle(result)
        

