import kodi_list
import kodi_container

container = kodi_container.Container()
container.load()

container.updateItems()

for item in container.ListItem:
    xbmc.log(msg="item: " + item.Label)
    xbmc.log(msg="item: " + item.FolderPath)
