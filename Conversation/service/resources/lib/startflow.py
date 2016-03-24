import os
import sys
import urlparse
import ConfigParser
from includes import kodion
import re

from resources.lib.flow.states import userInput
from resources.lib.flow.states import initial

import resources.lib.flow.contexts
#import resources.lib.flow

class Provider(kodion.AbstractProvider):
    def __init__(self, rootFolder):
        kodion.AbstractProvider.__init__(self)
        self.FolderSettings = FolderSettings(rootFolder)
        self.Config = ConfigParser.RawConfigParser()

        self.Config.read(self.FolderSettings.ConfigFile)

        self.AvailableContexts = {
                    "context": resources.lib.flow.contexts.Context,
                    "kodiContext": resources.lib.flow.contexts.KodiContext,
                    "kodiRemoteContext": resources.lib.flow.contexts.KodiRemoteContext,
                }

        self.AvailableStartStates = {
                    "userInput": resources.lib.flow.states.userInput.userInput,
                    "initial": resources.lib.flow.states.initial.initial,
                }
        self.log(msg="Starting flow provider!")
        #xbmcplugin.setProperty(int(sys.argv[1]), 'Emulator', 'M.A.M.E.')

    @kodion.RegisterProviderPath('^/(?P<context>.*)/keyboardinput/$')
    def on_phone_picked_up_during_keyboard(self, inputContext, re_match):
        self.log(msg="on_phone_picked_up_during_keyboard!")
        contextString = re_match.group('context')

        context = self.AvailableContexts[contextString](self.FolderSettings)
        context.State = resources.lib.flow.states.userInput.userInput(context)
        context.State.send_to_kodi_input(None)

    @kodion.RegisterProviderPath('^/(?P<context>.*)/(?P<start_state>.*)/$')
    def on_start_with_context(self, inputContext, re_match):
        self.log(msg="on_start_with_context!")
        userInputString = inputContext.get_param('user_input', '')
        contextString = re_match.group('context')
        startStateString = re_match.group('start_state')
        print (str(re_match.groups))
     
        context = self.AvailableContexts[contextString](self.FolderSettings)

        context.log("Here we go!")

        result = None

        if(startStateString is not None):
            context.log("Start state is " + startStateString)
            context.State = self.AvailableStartStates[startStateString](context)
        else:
            context.log("No start state. Exiting...")
            return None

        return context.State.handle(result)

    def on_search(self, search_text, context, re_match):
        raise NotImplementedError()

    def on_root(self, context, re_match):
        print (str(re_match))
        #return self.on_start_with_context(context, re_match)

    def log(self, msg):
        try:
            import xbmc 
            xbml.log(msg)
        except:
            print(msg)

class Test:
    def __init__(self, stringo):
        self.Url = urlparse.parse_qs(stringo)

    def get_param(self, param, default):
        if(param in self.Url):
            return self.Url[param][0]
        else:
            return default

class FolderSettings:
    def __init__(self, rootFolder):
        print("setting up folders:")
        self.RootFolder = rootFolder
        print("root folder: " + self.RootFolder)
        self.LibFolder = os.path.join(rootFolder, "resources", "lib")
        print("lib folder: " + self.LibFolder)
        self.IncludesDir = os.path.join(self.LibFolder, 'includes')
        print("includes folder: " + self.IncludesDir)
        self.ConfigFile = os.path.join(self.RootFolder, 'conversation.config')
        print("config file: " + self.ConfigFile)

#return result