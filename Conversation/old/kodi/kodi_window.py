import json
import kodi_json
import xbmcgui

class KodiWindow:
    def __init__(self, windowId = 0):
        if(windowId > 0):
            window = xbmcgui.Window(windowId)

        else:            
            window = kodi_json.kodi_execute_json({"method" : "GUI.GetProperties", "params" : { "properties" : ["currentwindow"]}})

            self.Id = int(window['result']['currentwindow']['id'])
            self.Label = window['result']['currentwindow']['label']

    def get_items(self):
        items = []
        itemsCount =  kodi_json.kodi_execute_json({"method" : "XBMC.GetInfoLabels", "params" : { "properties" : ["Container(0).NumItems"]}})
        for i in range(0, self.ItemCount):
            items.append('"Container(0).ListItem(' + str(i) + ').Label"')
            items.append('"Container(0).ListItem(' + str(i) + ').FolderPath"')
        
        # Next function the user should select an item
        self.NextFunction = self.select_and_play_item
        self.NeedsUserInput = True
        return '{"jsonrpc":"2.0","method":"XBMC.GetInfoLabels","id":"1","params":{"labels":[' + ','.join(items) + ']}}'