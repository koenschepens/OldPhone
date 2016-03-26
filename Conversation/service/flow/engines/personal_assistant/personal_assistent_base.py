import json
import os

__author__ = 'macbook'

class PersonalAssistantBase():
    def __init__(self, context):
        self.context = context

    def ask_text(self, what):
        print("you said: " + what)

    def open(self):
        pass

    def send(self, in_data, frame_count):
        pass

    def close(self):
        pass

    def getresponse(self):
        return self.request.getresponse()

    def get_json_response(self):
        response = self.getresponse()
        leJson = response.read()
        return json.loads(leJson)

class ImmediateResult:
    def executeAction(self, action):
        #{"jsonrpc":"2.0","method":"Input.ExecuteAction","params":{"action":"down"},"id":1}
        return '{"jsonrpc":"2.0","method":"Input.ExecuteAction","params":{"action":"' + action + '"},"id":1}'

class Result:
    def __init__(self, parsed_json):
        self.Id = 1000
        self.NextFunction = None
        self.NeedsUserInput = False
        self.Action = {}
        self.IncludesDir = os.path.dirname(os.path.realpath(__file__)) + '/includes/'
        self.ResolvedQuery = parsed_json

        '''if(parsed_json is None):
            #assume text only
            self.Text = parsed_json
            self.Action = "message.show"
            return;'''

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

