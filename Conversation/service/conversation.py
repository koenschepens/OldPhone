
import os.path, sys
import json
import subprocess 
import ConfigParser
import re

#activatewindow(video,plugin://plugin.video.kodipopcorntime/?searchString=asdf)"

folder = os.path.dirname(os.path.realpath(__file__))


try:
    import apiai
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
    import apiai

config = ConfigParser.RawConfigParser()
configFile = os.path.join(folder, 'conversation.config')
print "CONFIG FILE: " + configFile
config.read(configFile)

import time
import scipy.io.wavfile as wav

class Conversation:
    def __init__(self, client_access_token, subscription_key):
        self.client_access_token = client_access_token
        self.subscription_key = subscription_key
        self.Api = apiai.ApiAI(self.client_access_token, self.subscription_key)
        
    def ask(self, what):
        if(len(what) == 0):
            return self.get_show_notification_json("Sorry", "I didn't hear you...", 1)

        self.Request = what
        immediateActions = config.options("immediateActions")

        if(self.Request in immediateActions):
            configValue = config.get("immediateActions", self.Request)
           
            action = re.search('(\w*)\((\w*)\)', configValue)
            methodName = action.group(1)
            params = action.group(2)
            immediateResult = ImmediateResult()
            method = getattr(ImmediateResult, methodName)
            if not method:
                raise Exception("Method %s not implemented" % method_name)

            return method(immediateResult, params)

        request = self.Api.text_request()
        request.query = what
        response = request.getresponse()
        leJson = response.read()
        print (leJson)
        parsed_json = json.loads(leJson)

        result = Result(parsed_json)

        return result.getKodiAction()

    def get_show_notification_json(self, title, message, id):
        return '{ "jsonrpc": "2.0", "method": "GUI.infodialog", "params": { "title": "' + title + '", "message": "' + message + '" }, "id": ' + str(id) + ' }'

class ImmediateResult:
    def executeAction(self, action):
        return '{"jsonrpc":"2.0","method":"Input.ExecuteAction","params": { "Action" : "' + action + '" } ,"id":1}'

class Result:
    def __init__(self, parsed_json):
        self.ResolvedQuery = parsed_json['result']['resolvedQuery']
        self.IncludesDir = os.path.dirname(os.path.realpath(__file__)) + '/includes/'
        self.Text = parsed_json['result']['fulfillment']['speech']
        self.AvailableActions = config.options("actions")
        
        self.Action = {}
        if('action' in parsed_json['result']):
            self.Action = parsed_json['result']['action']

        self.Parameters = {}
        if('parameters' in parsed_json['result']):
            self.Parameters = parsed_json['result']['parameters']

    def getKodiAction(self):
        if(len(self.Action) > 0):
            print("action: " + str(self.Action))
            if(self.Action in self.AvailableActions):
                print("action found!")
                configValue = config.get("actions", self.Action)
                # ^(\w*)\(((\[\w*\])*)\)$
                action = re.search('(\w*)\((.*)\,*\)', configValue)
                methodName = action.group(1)

                print ("METHOD: " + methodName)
                params = self.updateParams(action.group(2).split(','))

                print ("PARAMS: " + str(params))
                method = getattr(self, methodName)
                if not method:
                    raise Exception("Method %s not implemented" % method_name)

                return method(params)

        func = self.other
        return func()

    def updateParams(self, params):
        paramsDict = {}

        for n, param in enumerate(params):
            splitted = params[n].split('=')
            name = splitted[0]
            value = splitted[1]

            if("q" in self.Parameters):
                value = value.replace("$q", self.Parameters["q"])
            if("location" in self.Parameters):
                value = value.replace("$location", self.Parameters["location"])
            if("service_name" in self.Parameters):
                value = value.replace("$service_name", self.Parameters["service_name"])

            value = value.replace("$speech", self.Text)

            paramsDict[name] = value

        return paramsDict

    def other(self):
        if(self.Text is not None):
            return self.get_show_notification_json(self.ResolvedQuery, self.Text, 600)
        else:
            return self.get_show_notification_json(self.ResolvedQuery, "Me no understand", 601)

    def songs(self):
         #if('q' in self.Parameters):
         return self.get_activatewindow_json("MusicLibrary", 501)

    def browser_open(self):
        return self.get_show_notification_json("Sorry", "Browsing the interwebs is not possible yet", 602)

    def playvideo(self, params):
        services = {
            'youtube': self.video_play_youtube,
            'movie' : self.video_play_popcorn_time
        }

        if('service_name' in params):
            func = services.get(params['service_name'], lambda: None)
            return func(params)
        else:
            return self.video_play_popcorn_time()

    def weather(self, params):
        return self.get_activatewindow_json("weather", 2)

    def video_play_popcorn_time(self):
        if('q' in self.Parameters):
            result = self.get_addon_json('plugin.video.kodipopcorntime', '"search": "' + self.Parameters['q'] + '"')
        elif('title' in self.Parameters):
            result = self.get_addon_json('plugin.video.kodipopcorntime', '"title" : "' + self.Parameters['title'] + '"')
        else:        
            result = self.get_addon_json('plugin.video.kodipopcorntime', '')
        return result + self.get_action("Down") + self.get_action("Select")

    def get_addon_json(self, addonid, params):
        return '{ "jsonrpc": "2.0", "method": "RunAddon", "params": { "wait": false, "addonid": "' + addonid + '", "params": { ' + params + ' } }, "id": 2 }'

    def runAddon(self, params):
        return '{ "jsonrpc": "2.0", "method": "RunAddon", "params": { "wait": false, "addonid": "' + addonid + '", "params": { ' + params + ' } }, "id": 2 }'

    def get_activatewindow_json(self, window, id):
        return '{ "jsonrpc": "2.0", "method": "ActivateWindow", "params": { "window": "' + window + '" }, "id": ' + str(id) + ' }'

    def get_show_notification_json(self, title, message, id):
        return '{ "jsonrpc": "2.0", "method": "ShowNotification", "params": { "title": "' + title + '", "message": "' + message + '" }, "id": ' + str(id) + ' }'

    def get_action(self, action):
        return '{ "jsonrpc": "2.0", "method": "' + action + '", "id": ' + str(4000) + ' }'

    def video_play_youtube(self, params):
        global includesDir
        if('searchQuery' not in params):
            self.LastMethod = self.video_play_youtube
            return "Nothing found"
        else:
            script = self.IncludesDir + 'youtube-search ' + params["searchQuery"]
            print(script)
            p = subprocess.Popen(script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            youtubeId, err = p.communicate()
            return '{"id":1,"jsonrpc":"2.0","method":"Player.Open","params":{"item":{"file":"plugin:\/\/plugin.video.youtube\/?path=\/root\/search&action=play_video&videoid=' + youtubeId + '"}}}'    

#tokens = { 'dutch' : 'b240ec13475a464890af46b48f49f5c7', 'english' : 'fb928615eb914f4785e110eecad49c95' }

#language = sys.argv[1]
#text = sys.argv[2]

#conversation = Conversation(tokens[language], '7c4c06c1-eb1d-4fd3-9367-134f20cbcb25')

#conversation.ask(text)