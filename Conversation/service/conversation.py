import os.path, sys
import json
import subprocess 
import ConfigParser
import re
import urllib
import urllib2
from urllib2 import HTTPError, URLError

reload(sys) 
sys.setdefaultencoding('UTF8')

folder = os.path.dirname(os.path.realpath(__file__))

try:
    import apiai
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
    import apiai

config = ConfigParser.RawConfigParser()
configFile = os.path.join(folder, 'conversation.config')
config.read(configFile)

client_access_token = config.get('aiapi', 'client_access_token')
subscription_key = config.get('aiapi', 'subscription_key')

import time
import scipy.io.wavfile as wav

class Conversation:
    def __init__(self):
        self.client_access_token = client_access_token
        self.subscription_key = subscription_key
        self.Api = apiai.ApiAI(self.client_access_token, self.subscription_key)

    def ask(self, what):
        if(len(what) == 0):
            self.Result = Result("Sorry, I didn't hear you")
            return self.Result

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
    def __init__(self, parsed_json, client_access_token = None, subscription_key = None):
        self.Id = 1000
        self.NextFunction = None
        self.NeedsUserInput = False
        self.Action = {}
        self.IncludesDir = os.path.dirname(os.path.realpath(__file__)) + '/includes/'
        self.ResolvedQuery = parsed_json   

        if(client_access_token is None):
            #assume text only
            self.Text = parsed_json
            self.Action = "message.show"
            return;

        self.client_access_token = client_access_token
        self.subscription_key = subscription_key
        self.ResolvedQuery = parsed_json['result']['resolvedQuery']
        self.Text = parsed_json['result']['fulfillment']['speech']
        self.ParsedJson = parsed_json

        if('action' in parsed_json['result']):
            self.Action = parsed_json['result']['action']
        else:
            self.Action = "input.unknown"

        self.Parameters = {}
        if('parameters' in parsed_json['result']):
            self.Parameters = parsed_json['result']['parameters']

    def __str__(self):
        result = ""
        for slot in dir(self):
            attr = getattr(self, slot)
            result = result + "\r\n" + slot + ": " + str(attr)
        return result

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

#conversation.ask(text)