import context
import logging
import time
try:
    from xbmc.xbmcclient import XBMCClient,ACTION_EXECBUILTIN,ACTION_BUTTON
except:
    sys.path.append('/usr/share/pyshared/xbmc')
    from xbmcclient import XBMCClient,ACTION_EXECBUILTIN,ACTION_BUTTON

# Use this context to create a remote connection with kodi
class KodiRemoteContext(context.Context):
    def __init__(self, folder):
        context.Context.__init__(self, folder)

        host = self.Config.get("xbmc", "host")
        port = self.Config.getint("xbmc", "port")

        # Create an XBMCClient object and connect (needed because we don't run as the same user as Kodi)
        self.Xbmc = XBMCClient("kodiRemoteContext")
        self.Xbmc.connect()

    def log(self, message):
        if(self.Xbmc is not None):
            self.Xbmc.send_log(3, message)
        logging.log(1, message)

    def ActivateWindow(self, pluginurl = None, window = 'videos'):
        if(pluginurl is None):
            action = 'ActivateWindow(' + window + ')'
        else:
            action = 'ActivateWindow(' + window + ',' + pluginurl + ')'
        self.send_action(action)

    def send_action(self, action):
        self.log("sending action: " + action)
        self.Xbmc.send_action(action, ACTION_EXECBUILTIN)

    def show_notification(self, title, message = ''):
        self.log("sending notification: " + title + "," + message)        
        self.Xbmc.send_notification(title=title, message=message, icon_file=None)
