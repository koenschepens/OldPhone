import xbmc, xbmcgui
 
#get actioncodes from https://github.com/xbmc/xbmc/blob/master/xbmc/guilib/Key.h
ACTION_PREVIOUS_MENU = 10
ACTION_SELECT_ITEM = 7
 
class KeyPad(xbmcgui.Window):
    def __init__(self):
        self.buttonSize = 200
        self.padding = 20
        self.items = []
        self.list = xbmcgui.ControlList(200, 150, 300, 400)
        pass

    def addItems(self, items):
        i = 0
        self.items = items
        for item in items:
            listItem = xbmcgui.ListItem()
            listItem.setLabel(item['label'])
            listItem.setPath(item['path'])
            self.list.addItem(listItem)
            
            self.strActionInfo = xbmcgui.ControlLabel(((self.padding + self.buttonSize) * (i % 3) + 1),((i / 3) + 1) * self.buttonSize, self.buttonSize, self.buttonSize, str(item['number']), 'font26', '0xFFBBFFBB')
            i = i + 1

        self.addControl(self.list) 

    def onAction(self, action):
        if action == ACTION_PREVIOUS_MENU:
            self.close()
        if action == ACTION_SELECT_ITEM:
            xbmc.log("action: " + str(action.getButtonCode()), level = xbmc.LOGWARNING)
            xbmc.log("action: " + self.list[action.getButtonCode()], level = xbmc.LOGWARNING)
        else:
            xbmc.log("Unknown action " + str(action.getId()), level = xbmc.LOGWARNING)

    def onControl(self, control):
        if control == self.list:
            item = self.list.getSelectedItem()
            self.message('You selected : ' + item.getLabel()) 