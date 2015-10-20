import json
import kodi_json

class ListItem:
    Label = ''
    Label2 = ''
    FolderPath = ''

    def play(self):
        params = { "method" : "Player.Open", "params" : { "item" : { "file" : self.FolderPath }}}
        kodi_json.kodi_execute_json(params)
