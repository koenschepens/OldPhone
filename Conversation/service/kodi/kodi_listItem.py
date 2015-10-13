import json

class ListItem:
    Label = ''
    Label2 = ''
    FolderPath = ''

    def __init__(self, label, folderPath):
        self.Label = label
        self.FolderPath = folderPath