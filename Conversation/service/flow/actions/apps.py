import ConfigParser
from service.flow.states.statebase import StateBase

try:
    import xbmcgui
except:
    pass

class apps(StateBase):

    def handle(self, result):
        self.Config = ConfigParser.RawConfigParser()
        configFile = 'actions.config'
        self.log(configFile)
        self.Config.read(configFile)

    def open(self, result):
        appName = str(result.Parameters['app_name'])

        if(appName in self.Config.options("apps")):
            appId = self.context.Config.get("apps", appName)
            self.context.log("open app: " + appId)
            self.context.open_plugin(pluginurl = appId)



       