from service import kodi
import target_base
import sys
import time

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
        class xbmc():
            LOGDEBUG = 0
            LOGWARNING = 1
            LOGERROR = 2

        WINDOW_DIALOG_TEXT_VIEWER = 4
        pass

class Kodi(target_base.TargetBase):
    Config = None
    def __init__(self, context):
        target_base.ContextBase.__init__(self, context.folder)
     
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
        self.activate_window(WINDOW_DIALOG_TEXT_VIEWER)

    def get_json_result(self, query):
        xbmcResult = self.Context.xbmc.executeJSONRPC(query.encode('utf8'))

        if(self.Context.log(xbmcResult['status']['code'] == '200')):
            self.Context.log("succes! " + str(xbmcResult))
        else:
            self.Context.log("error! result.ParsedJson: " + str(xbmcResult.ParsedJson) + ". Kodi response: " + str(xbmcResult))

        return xbmcResult

    def activate_window(self, pluginurl = None, window = 'videos'):
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

    def user_input_required(self):
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

    def get_show_notification_json(self, title, message, id):
        return '{ "jsonrpc": "2.0", "method": "GUI.ShowNotification", "params": { "title": "' + title + '", "message": "' + message + '" }, "id": ' + str(id) + ' }'
