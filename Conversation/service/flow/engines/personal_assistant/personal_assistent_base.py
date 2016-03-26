import json
import os

__author__ = 'macbook'

class PersonalAssistantBase():
    def __init__(self, context):
        self.context = context
        self._active = True

    def is_active(self):
        return self._active

    def ask_text(self, what):
        print("you said: " + what)

    def open(self):
        pass

    def send(self, in_data, frame_count):
        pass

    def close(self):
        pass

    def getresponse(self):
        return self.request.getresponse().read()

    def get_json_response(self):
        return json.loads(self.getresponse())

    def get_result(self):
        raise NotImplementedError

class ImmediateResult:
    def executeAction(self, action):
        #{"jsonrpc":"2.0","method":"Input.ExecuteAction","params":{"action":"down"},"id":1}
        return '{"jsonrpc":"2.0","method":"Input.ExecuteAction","params":{"action":"' + action + '"},"id":1}'

class AssistentResult():
    Id = 0
    NextFunction = None
    NeedsUserInput = False
    Action = {}
    IncludesDir = None
    ResolvedQuery = None
    Text = None
    Action = None
    Parameters = {}
    Url = None

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

            # TODO : I can do better than this:
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

