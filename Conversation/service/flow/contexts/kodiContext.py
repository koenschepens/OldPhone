import context
import sys
import kodi
import time
import kodiContextFiles

try:
    import xbmcgui
    import xbmcplugin
    import xbmc, xbmcaddon
except:
    sys.path.append('/usr/share/pyshared/xbmc')
    try:
        from xbmcclient import XBMCClient,ACTION_EXECBUILTIN,ACTION_BUTTON
        import xbmcgui
        import xbmcplugin
        import xbmc, xbmcaddon
    except:
        pass

class KodiContext(context.Context):
    Config = None
    def __init__(self, folder):
        context.Context.__init__(self, folder)
     
    def log(self, text, logType = "warning"):
        logTypes = { 
            "debug": xbmc.LOGDEBUG,
            "error": xbmc.LOGERROR,
            "warning": xbmc.LOGWARNING
        }

        xbmc.log(msg= "[state: " + self.State.__class__.__name__ + "]: " + text, level=logTypes[logType])

    def show_notification(self, title, message = ''):
        dialog = xbmcgui.Dialog()
        dialog.notification(title, message, xbmcgui.NOTIFICATION_INFO, 5000)

    def show_text(self, title):
        self.ActivateWindow(WINDOW_DIALOG_TEXT_VIEWER)

    def get_json_result(self, query):
        xbmcResult = self.Context.xbmc.executeJSONRPC(query.encode('utf8'))

        if(self.Context.log(xbmcResult['status']['code'] == '200')):
            self.Context.log("succes! " + str(xbmcResult))
        else:
            self.Context.log("error! result.ParsedJson: " + str(result.ParsedJson) + ". Kodi response: " + str(xbmcResult))

        return xbmcResult

    def ActivateWindow(self, pluginurl = None, window = 'videos'):
        if(pluginurl is None):
            action = 'ActivateWindow(' + window + ')'
        else:
            action = 'ActivateWindow(' + window + ',' + pluginurl + ')'

        result = self.send_action(action)
        
        container = kodi.Container()
        container.load()
        container.updateItems()

        return container

    def send_action(self, action):
        self.log("sending action: " + action)
        xbmc.executebuiltin(action)

    def userInputRequired(self):
        self.log("check if user input is required")
        time.sleep(8)
        win = xbmcgui.WindowDialog()

        #self.log("controlList.size: " + str(controlList.size()))
        numberOfItems = int(xbmc.getInfoLabel("Container().NumItems"))

        items = []

        for i in xrange(1,numberOfItems):
            skip = 0
            label = xbmc.getInfoLabel("Container().ListItem(" + str(i) + ").Label")
            items.append({ "label": label, "number" : i })

        mydisplay = kodiContextFiles.KeyPad.KeyPad()
        mydisplay.addItems(items)
        mydisplay.doModal()

            #win.setProperty("Container().ListItem(" + str(i) + ").Label", "[" + str(i) + "] " + label )
        return numberOfItems > 1
    