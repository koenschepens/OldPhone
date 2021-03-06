import target_base
import logging
import time
import sys
try:
    from xbmc.xbmcclient import XBMCClient,ACTION_EXECBUILTIN,ACTION_BUTTON
except:
    try:
        sys.path.append('/usr/share/pyshared/xbmc')
        from xbmcclient import XBMCClient,ACTION_EXECBUILTIN,ACTION_BUTTON
    except:
        import xbmc_client as xbmcclient

# Use this context to create a remote connection with target
class KodiRemote(target_base.ContextBase):
    def __init__(self, folder):
        target_base.ContextBase.__init__(self, folder)

        host = self.Config.get("xbmc", "host")
        port = self.Config.getint("xbmc", "port")

        # Create an XBMCClient object and connect (needed because we don't run as the same user as Kodi)

    def log(self, message):
        print(self.State.__class__.__name__ + ": " + message)
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
        xbmcClient = XBMCClient("floeps")
        xbmcClient.connect()
        time.sleep(1)
    
        self.log("sending action: " + action)
        xbmcClient.send_action(action, ACTION_EXECBUILTIN)

    def show_notification(self, title, message = ''):
        self.log("sending notification: " + title + "," + message)        
        self.Xbmc.send_notification(title=title, message=message, icon_file=None)

    def get_window(self):
        return None

    def user_input_required(self):
        win = xbmcgui.Window(xbmcgui.getCurrentWindowId())
        numberOfItems = xbmc.getProperty("Container().NumItems")
        if(numberOfItems > 9):
            numberOfItems = 9
        for i in xrange(1,numberOfItems):
            label = xbmc.getProperty("Container().ListItem(" + str(i) + ").Label")
            xbmc.setProperty("Container().ListItem(" + str(i) + ").Label", "[" + str(i) + "] " + label )
        return numberOfItems > 1
    
