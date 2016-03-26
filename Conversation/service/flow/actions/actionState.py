from Conversation.service.flow.actions import media, smalltalk, weather, news, input as Input, images, message, clock, name, apps, wisdom
from Conversation.service.flow.actions.configActionState import configActionState as cs
from Conversation.service.flow.states.statebase import StateBase

class actionState(StateBase):
    def handle(self, result):
        immediateActions = self.context.config.options("immediateActions")

        if(isinstance(result, basestring)):
            self.context.State = cs(self.context)
            self.context.State.handle(result)
            return

        configState = cs(self.context)

        if(not configState.handle(result)):
            self.context.log(result.Action + " is not a config item")

            self.context.log("Action: " + str(result.Action))

            actionItems = result.Action.split('.')
            actionClassess = {
                "media": media.media,
                "wisdom": wisdom.wisdom,
                "smalltalk": smalltalk.smalltalk,
                "weather": weather.weather,
                "news": news.news,
                "input": Input.input,
                "images": images.images,
                "message": message.message,
                "clock": clock.clock,
                "name": name.name,
                "apps": apps.apps
            }

            if(actionItems[0] in actionClassess):
                self.context.log("domain exists :" + actionItems[0])
                self.context.State = actionClassess[actionItems[0]](self.context)
            else:
                self.context.log("domain " + actionItems[0] + " does not exist. Using config")
                self.context.State = cs(self.context)

            if(hasattr(self.context.State, actionItems[1])):
                self.context.log("actionState action: " + actionItems[1])
                action = getattr(self.context.State, actionItems[1])
                action(result)
            else:
                self.context.log("action does not exist: " + actionItems[1] + ". Using " + self.context.State.__class__.__name__ + ".handle()")
                self.context.State.handle(result)

        # Check if user input is required
        if(self.context.user_input_required()):
            self.context.State = input(self.context)
            self.context.State.handle(result)


