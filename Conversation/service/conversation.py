import os.path, sys
import json
import subprocess 
import ConfigParser
import re
import urllib
from urllib2 import urlopen, URLError, HTTPError

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

        self.Result = Result(parsed_json, self.client_access_token, self.subscription_key)

        return self.Result

    def get_show_notification_json(self, title, message, id):
        return '{ "jsonrpc": "2.0", "method": "GUI.ShowNotification", "params": { "title": "' + title + '", "message": "' + message + '" }, "id": ' + str(id) + ' }'

class ImmediateResult:
    def executeAction(self, action):
        #{"jsonrpc":"2.0","method":"Input.ExecuteAction","params":{"action":"down"},"id":1}
        return '{"jsonrpc":"2.0","method":"Input.ExecuteAction","params":{"action":"' + action + '"},"id":1}'

class Result:
    def __init__(self, parsed_json, client_access_token, subscription_key):
        self.client_access_token = client_access_token
        self.subscription_key = subscription_key
        self.ResolvedQuery = parsed_json['result']['resolvedQuery']
        self.IncludesDir = os.path.dirname(os.path.realpath(__file__)) + '/includes/'
        self.Text = parsed_json['result']['fulfillment']['speech']
        self.AvailableActions = config.options("actions")
        self.Id = 1000
        
        self.Action = {}
        if('action' in parsed_json['result']):
            self.Action = parsed_json['result']['action']

        self.Parameters = {}
        if('parameters' in parsed_json['result']):
            self.Parameters = parsed_json['result']['parameters']
    
    def getAudioStream(self):
        fileLocation = folder + "/output.wav"
        url = 'https://api.api.ai/v1/tts?v=20150910&text=' + urllib.quote(self.Text)
        req = urllib2.Request(url)
        req.add_header('ocp-apim-subscription-key', self.subscription_key)
        req.add_header('Authorization', 'Bearer ' + self.client_access_token)
        r = urllib2.urlopen(req)
        try:
            # Open our local file for writing
            with open(fileLocation, "wb") as local_file:
                local_file.write(r.read())

        #handle errors
        except HTTPError, e:
            print "HTTP Error:", e.code, url
        except URLError, e:
            print "URL Error:", e.reason, url

        return self.playUrl(fileLocation)

    def getKodiAction(self):
        self.Id = self.Id + 1
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
            if("genre" in self.Parameters):
                value = value.replace("$genre", self.Parameters["genre"])
            if("service_name" in self.Parameters):
                value = value.replace("$service_name", self.Parameters["service_name"])
            else:
                value = value.replace("$service_name", 'popcorntime')

            if("title" in self.Parameters):
                value = value.replace("$q", self.Parameters["title"])
                value = value.replace("$title", self.Parameters["title"])
                value = value.replace("$service_name", 'popcorntime')

            value = value.replace("$speech", self.Text)
            value = value.replace("$resolvedQuery", self.ResolvedQuery)

            paramsDict[name] = value

        return paramsDict

    def other(self):
        if(self.Text is not None):
            return self.show_notification(self.ResolvedQuery, self.Text, 600)
        else:
            return self.show_notification(self.ResolvedQuery, "Me no understand", 601)

    def songs(self):
         #if('q' in self.Parameters):
         return self.get_activatewindow_json("MusicLibrary", 501)

    def browser_open(self):
        return self.get_show_notification_json("Sorry", "Browsing the interwebs is not possible yet", 602)

    def playvideo(self, params):
        services = {
            'youtube': self.video_play_youtube,
            'popcorntime' : self.video_play_popcorn_time
        }

        if('service_name' in params):
            func = services.get(params['service_name'], lambda: None)
            return func(params)
        else:
            return self.video_play_popcorn_time(params)

    def weather(self, params):
        return self.get_activatewindow_json("weather", 2)

    def video_play_popcorn_time(self, params):
        if('title' in params and params['title'] != '$title'):
            q = params['title']
            result = '{"id":1,"jsonrpc":"2.0","method":"GUI.ActivateWindow","params":{"window":"videos","parameters":["plugin://plugin.video.kodipopcorntime/search?query=' + q + '"]}}'
        elif('searchQuery' in params and params['searchQuery'] != '$q'):
            q = params['searchQuery']
            result = '{"id":1,"jsonrpc":"2.0","method":"GUI.ActivateWindow","params":{"window":"videos","parameters":["plugin://plugin.video.kodipopcorntime/search?query=' + q + '"]}}'
        elif('genre' in params):
            result = '{"id":1,"jsonrpc":"2.0","method":"GUI.ActivateWindow","params":{"window":"videos","parameters":["plugin://plugin.video.kodipopcorntime/genres/' + params['genre'] + '/0?limit=20"]}}'

        return result

    def get_addon_json(self, addonid, params):
        return '{ "jsonrpc": "2.0", "method": "Addons.ExecuteAddon", "params": { "wait": false, "addonid": "' + addonid + '", "params": ' + json.dumps(params) + ' }, "id": 2 }'

    def get_activatewindow_json(self, window, id):
        return '{ "jsonrpc": "2.0", "method": "ActivateWindow", "params": { "window": "' + window + '" }, "id": ' + str(self.Id) + ' }'

    def show_notification(self, params):
        return '{ "jsonrpc": "2.0", "method": "GUI.ShowNotification", "params": ' + json.dumps(params) + ', "id": ' + str(self.Id) + ' }'

    def show_notification(self, title, message, id):
        return '{ "jsonrpc": "2.0", "method": "GUI.ShowNotification", "params": { "title": "' + title + '", "message": "' + message + '" }, "id": ' + str(id) + ' }'

    def playUrl(self, url):
        params = { "method": "Player.Open", "item": { "file" : urllib.quote(url) }}
        return self.json(params)

    def json(self, params):
        method = params['method']
        del params["method"]
        return '{ "jsonrpc": "2.0", "method": "' + method + '", "params": ' + json.dumps(params) + ', "id": ' + str(self.Id) + ' }'

    def get_action(self, action):
        return '{ "jsonrpc": "2.0", "method": "' + action + '", "id": ' + str(4000) + ' }'

    def video_play_youtube(self, params):
        global includesDir
        if('searchQuery' not in params):
            self.LastMethod = self.video_play_youtube
            return "Nothing found"
        else:
            script = self.IncludesDir + 'youtube-search ' + params["searchQuery"]
            p = subprocess.Popen(script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            youtubeId, err = p.communicate()
            return '{"id":1,"jsonrpc":"2.0","method":"Player.Open","params":{"item":{"file":"plugin:\/\/plugin.video.youtube\/?path=\/root\/search&action=play_video&videoid=' + youtubeId + '"}}}'    

#tokens = { 'dutch' : 'b240ec13475a464890af46b48f49f5c7', 'english' : 'fb928615eb914f4785e110eecad49c95' }

#language = sys.argv[1]
#text = sys.argv[2]

#conversation = Conversation(tokens[language], '7c4c06c1-eb1d-4fd3-9367-134f20cbcb25')

#conversation.ask(text)