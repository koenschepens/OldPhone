import flow
from flow import state
from flow.actions import *
from flow.actions import configActionState
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

        configState = configActionState.configActionState(self.Context)

        if(not configState.handle(result)):
            self.Context.log(result.Action + " is not a config item")

            #for item in dir(result):
            #    self.Context.log(str(getattr(result, item)))
            self.Context.log("Action: " + str(result.Action))

            actionItems = result.Action.split('.')
            actionClassess = {
                "media": flow.actions.media,
                "smalltalk": flow.actions.smalltalk,
                "weather": flow.actions.weather,
                "news": flow.actions.news,
                "smalltalk": flow.actions.smalltalk,
                "input": flow.actions.input,
                "images": flow.actions.images,
                "message": flow.actions.message,
                "clock": flow.actions.clock,
                "name": flow.actions.name,
                "apps": flow.actions.apps
            }

            if(actionItems[0] in actionClassess):
                self.Context.log("domain exists :" + actionItems[0])
                self.Context.State = actionClassess[actionItems[0]](self.Context)
            else:
                self.Context.log("domain " + actionItems[0] + " does not exist. Using config")
                self.Context.State = flow.actions.configAction(self.Context)
            
            if(hasattr(self.Context.State, actionItems[1])):
                self.Context.log("actionState action: " + actionItems[1])
                action = getattr(self.Context.State, actionItems[1])
                action(result)
            else:
                self.Context.log("action does not exist: " + actionItems[1] + ". Using " + self.Context.State.__class__.__name__ + ".handle()")
                self.Context.State.handle(result)

        # Check if user input is required
        if(self.Context.userInputRequired()):
            self.Context.State = flow.actions.input(self.Context)
            self.Context.State.handle(result)
        

