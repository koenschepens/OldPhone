import resources.lib.flow.states.abstract_state
import resources.lib.flow.contexts
import resources.languages.languageparser
import datetime
import ConfigParser
import json

import resources.lib.conversation
from actionState import actionState

import time

class language(actionState):

    def switch(self, result):
        config = ConfigParser.SafeConfigParser()
        config.read(self.Context.FolderSettings.ConfigFile)
        lang = result.Parameters['language']['langCode']
        config.set('settings', 'language', lang)

        with open(self.Context.FolderSettings.ConfigFile, 'wb') as configfile:
            config.write(configfile)

        self.Context._setup()

        response = resources.languages.languageparser.getText(id="language_switched", lang=lang)
        
        self.Context.show_notification(response)
        self.Context.say(response)
        
        return True
