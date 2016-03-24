import context
import sys
#import kodi
import time
import json

try:
    import xbmcgui
    import xbmcplugin
    import xbmc, xbmcaddon
    import kodiContextFiles
except:
    sys.path.append('/usr/share/pyshared/xbmc')
    try:
        from xbmcclient import XBMCClient,ACTION_EXECBUILTIN,ACTION_BUTTON
        import xbmcgui
        import xbmcplugin
        import xbmc, xbmcaddon
    except:
        class xbmc():
            LOGDEBUG = 0
            LOGWARNING = 1
            LOGERROR = 2

        WINDOW_DIALOG_TEXT_VIEWER = 4
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

        xbmc.log(msg= "KodiContext: [state: " + str(self.State.__class__.__name__) + "]: " + str(text), level=logTypes[logType])

    def show_notification(self, title, message = ''):
        dialog = xbmcgui.Dialog()
        dialog.notification(title, message, xbmcgui.NOTIFICATION_INFO, 5000)

    def show_text(self, title):
        self.ActivateWindow(WINDOW_DIALOG_TEXT_VIEWER)

    def get_json_result(self, query):
        xbmcResult = json.loads(xbmc.executeJSONRPC(query.encode('utf8')))

        self.log(str(xbmcResult))
        return xbmcResult

    def input_send(self, text):
        return self.get_json_result('{ "jsonrpc": "2.0", "method": "GUI.ShowNotification", "params": { "title": "' + title + '", "message": "' + message + '" }, "id": ' + str(id) + ' }')

    def ActivateWindow(self, pluginurl = None, window = 'videos'):
        if(pluginurl is None):
            action = 'ActivateWindow(' + window + ')'
        else:
            action = 'ActivateWindow(' + window + ',' + pluginurl + ')'

        result = self.send_action(action)
        
    def send_action(self, action):
        self.log("sending action: " + action)
        xbmc.executebuiltin(action)

    def userInputRequired(self):
        self.log("check if user input is required")
        """win = xbmcgui.WindowDialog()
        numberOfItems = 0

        #self.log("controlList.size: " + str(controlList.size()))
        numberOfItemsLabel = xbmc.getInfoLabel("Container().NumItems")
        
        if(numberOfItemsLabel is not None and len(numberOfItemsLabel) > 0):
            numberOfItems = int(numberOfItemsLabel)

            items = []
            for i in xrange(1,numberOfItems):
                skip = 0
                label = xbmc.getInfoLabel("Container().ListItem(" + str(i) + ").Label")
                thumb = xbmc.getInfoLabel("Container().ListItem(" + str(i) + ").Thumb")
                path = xbmc.getInfoLabel("Container().ListItem(" + str(i) + ").Path")
                items.append({ "label": label, "number" : i, "thumbnail" : thumb, "path" : path })

            mydisplay = kodiContextFiles.KeyPad.KeyPad()
            mydisplay.addItems(items)
            mydisplay.doModal()"""

            #win.setProperty("Container().ListItem(" + str(i) + ").Label", "[" + str(i) + "] " + label )
        return numberOfItems > 1
    