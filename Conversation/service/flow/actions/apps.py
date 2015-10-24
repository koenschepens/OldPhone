import flow.state
import flow.initial
import flow.contexts
import flow.actions
import kodi
try:
    import xbmcgui
except:
    pass
import time

import conversation
from actionState import actionState
from userInput import userInput

class apps(actionState):

    def handle(self, result):
        self.Config = ConfigParser.RawConfigParser()
        configFile = 'actions.config'
        self.log(configFile)
        self.Config.read(configFile)

    def open(self, result):
        appName = str(result.Parameters['app_name'])

        if(appName in self.Config.options("apps")):
            appId = self.Context.Config.get("apps", appName)
            self.Context.log("open app: " + appId)
            self.Context.ActivateWindow(pluginurl = appId)



       