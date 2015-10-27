import resources.lib.flow.states.abstract_state
import resources.lib.flow.contexts
import resources.lib.flow.states
try:
    import xbmcgui
except:
    pass
import time

import resources.lib.conversation
from resources.lib.flow.states.actionState import actionState
from resources.lib.flow.states.userInput import userInput

class apps(actionState):

    def handle(self, result):
        self.Config = ConfigParser.RawConfigParser()
        configFile = 'actions.config'
        self.log(configFile)
        self.Config.read(configFile)
        return None

    def open(self, result):
        appName = str(result.Parameters['app_name'])

        if(appName in self.Config.options("apps")):
            appId = self.Context.Config.get("apps", appName)
            self.Context.log("open app: " + appId)
            self.Context.ActivateWindow(pluginurl = appId)



       