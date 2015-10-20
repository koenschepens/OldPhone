import flow.state
import flow.contexts

import conversation
import sys
from actionState import actionState

class weather(actionState):

    def handle(self, result):
        self.Context.log(str(result.Parameters))

    def search(self, result):
        self.Context.log("weather search: " + str(result.Parameters))

        if("location" in result.Parameters):
            #try:
            sys.path.append('/home/osmc/.kodi/addons/weather.yahoo/')
            sys.path.append('/home/osmc/.kodi/addons/weather.yahoo/resources/lib')
            import default

            #self.Context.ActivateWindow(pluginurl = None, window = "weather")
            locname = result.Parameters["location"]
            locid = find_location(locname)
            forecast(locname, locide)
            #except:
            #    self.Context.log("error loading weather")
            #    self.Context.ActivateWindow(pluginurl = None, window = "weather")
        else:
            self.Context.ActivateWindow(pluginurl = None, window = "weather")
