import kodi_json
import kodi_infoLabelObject
import kodi_listItem
import xbmc
import json

class Container(kodi_infoLabelObject.InfoLabelObject):
    Viewmode = ''
    FolderPath = ''
    FolderName = ''
    SortMethod = ''
    PluginName = ''
    PluginCategory = ''
    ShowPlot = ''
    NumPages = 0
    #Number of items in the container with given id. If no id is specified it grabs the current container
    NumItems = 0
    ListItem = []

    #Current page in the container with given id. If no id is specified it grabs the current container.
    CurrentPage = 0
    #Current item in the container with given id. If no id is specified it grabs the current container.
    CurrentItem = ''
    #Returns the current focused position of Container (id) as a numeric label.
    Position = ''
    Totaltime = 0

    def updateItems(self):
        self.loadItems("ListItem", self.NumItems, self.ListItem, kodi_listItem.ListItem)

    def hasItems(self):
        return self.NumItems > 1

    def getItemByLabel(self, label):
        for item in self.ListItem:
            if(item.Label.lower() == label.lower()):
                return item

    def getItemByPosition(self, position):
        return self.ListItems[position]
                
