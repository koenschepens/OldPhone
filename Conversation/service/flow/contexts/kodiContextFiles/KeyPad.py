import xbmc, xbmcgui
 
#get actioncodes from https://github.com/xbmc/xbmc/blob/master/xbmc/guilib/Key.h
ACTION_PREVIOUS_MENU = 10
ACTION_SELECT_ITEM = 7
 
class KeyPad(xbmcgui.Window):
    def __init__(self):
        self.buttonSize = 200
        self.padding = 20
        pass

    def addItems(self, items):
        i = 0
        for item in items:
            self.addControl(xbmcgui.ControlButton(((self.padding + self.buttonSize) * (i % 3) + 1),((i / 3) + 1) * self.buttonSize, self.buttonSize, self.buttonSize, item['label'], 'font17', '0xFFBBFFBB'))
            self.strActionInfo = xbmcgui.ControlLabel(((self.padding + self.buttonSize) * (i % 3) + 1),((i / 3) + 1) * self.buttonSize, self.buttonSize, self.buttonSize, str(item['number']), 'font26', '0xFFBBFFBB')
            i = i + 1

    def onAction(self, action):
        if action == ACTION_PREVIOUS_MENU:
            self.close()
