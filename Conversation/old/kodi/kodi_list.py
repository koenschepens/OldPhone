import xbmc
import kodi_json
import json

class ListItems:
    Items = {}

    """
    def get_current_window(self):
        return '{jsonrpc"":"2.0","method":"GUI.GetProperties","id":"1","params":{"properties":["currentwindow"]}}'

    def get_number_of_items(self, params):
        self.NextFunction = self.get_items
        return '{"jsonrpc":"2.0","method":"XBMC.GetInfoLabels","id":"1","params":{"labels":["Container(0).NumItems"]}}'

    def select_and_play_item(self, item):
        self.NextFunction = None
        self.NeedsUserInput = False

        print("Gekozen voor: " + item["Label"])

        params = { "method" : "Player.Open", "params" : { "item" : { "file" : item["FolderPath"] }}}

        return self.json(params)

    def get_items(self, params, attempt = 0):
        if(attempt > 5):
            self.NextFunction = None
            self.NeedsUserInput = False
            return None

        try:
            numberOfItems = int(json.loads(params)['result']['Container(0).NumItems'])

            items = []
            for i in range(0, numberOfItems):
                items.append('"Container(0).ListItem(' + str(i) + ').Label"')
                items.append('"Container(0).ListItem(' + str(i) + ').FolderPath"')
            
            # Next function the user should select an item
            self.NextFunction = self.select_and_play_item
            self.NeedsUserInput = True
            return '{"jsonrpc":"2.0","method":"XBMC.GetInfoLabels","id":"1","params":{"labels":[' + ','.join(items) + ']}}'
        except:
            # Maybe we should wait and try again
            sleep(attempt)
            return self.get_items(params, attempt + 1)
"""
