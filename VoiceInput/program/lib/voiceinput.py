import sys
import xbmc, xbmcgui, xbmcaddon
try:
    import simplejson
except ImportError:
    import json as simplejson
import httplib

__addon__      = xbmcaddon.Addon()
__cwd__        = __addon__.getAddonInfo('path').decode("utf-8")
__language__   = __addon__.getLocalizedString

class InputWindow(xbmcgui.WindowXMLDialog):
    def __init__( self, *args, **kwargs ):
        self.Kodi14 = False
        self.CTL_NUM_START = 48
        self.CTL_NUM_END   = 57
        self.CTL_LABEL_EDIT = 310
        self.strEdit = kwargs.get("default").decode('utf-8') or u""
        self.strHeading = kwargs.get("heading") or ""
        self.bIsConfirmed = False
        self.oldPhone = True
        self.keyType = LOWER
        self.words = []
        self.hzcode = ''
        self.pos = 0
        self.num = 0
        xbmcgui.WindowXMLDialog.__init__(self)
        xbmc.log(msg="HEE HALLO@!!", level=xbmc.LOGDEBUG)
    
    def initControl(self):
        pEdit = self.getControl(self.CTL_LABEL_EDIT)
        px = pEdit.getX()
        py = pEdit.getY()
        pw = pEdit.getWidth()
        ph = pEdit.getHeight()
        self.listw = pw - 95
        self.CTL_HZCODE = xbmcgui.ControlLabel(px, py + ph, 90, 30, '')
        self.CTL_HZLIST = xbmcgui.ControlLabel(px + 95, py + ph, pw - 95, 30, '')
        self.addControl(self.CTL_HZCODE)
        self.addControl(self.CTL_HZLIST)

    def getText(self):
        return "MONGOL!"

class Keyboard:
    def __init__( self, default='', heading='' ):
        self.bIsConfirmed = False
        self.strEdit = default
        self.strHeading = heading

    def doModal (self):
        self.win = InputWindow("DialogKeyboard.xml", __cwd__, heading=self.strHeading, default=self.strEdit )
        self.win.doModal()
        self.bIsConfirmed = self.win.isConfirmed()
        self.strEdit = self.win.getText()
        del self.win

    def setHeading(self, heading):
        self.strHeading = "WHOWHOWWWWOOOOO"

    def isConfirmed(self):
        return self.bIsConfirmed

    def getText(self):
        return "youtube"