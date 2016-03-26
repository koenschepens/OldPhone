import os
import sys
from Conversation.service.flow.engines.personal_assistant.personal_assistent_base import PersonalAssistantBase, \
    AssistentResult

actionMapper = {
    "NoResultCommand" : "wisdom.unknown",
    "WikipediaCommand" : "browser.open"
}

__author__ = 'macbook'

from Conversation.includes.houndify.houndify import HoundListener, StreamingHoundClient

class HoundifyEngine(PersonalAssistantBase, HoundListener):
    def __init__(self, context):
        self.context = context
        self.client_id = context.config.get("houndify", "client_id")
        self.client_key = context.config.get("houndify", "client_key")

    def ask_text(self, what):
        print("you said: " + what)

    def open(self):
        self.client = StreamingHoundClient(self.client_id, self.client_key, sampleRate=8000)
        self.client.setLocation(37.388309, -121.973968)
        self._active = True
        self.client.start(self)

    def send(self, in_data, frame_count):
        self._active = not self.client.fill(in_data)

    def close(self):
        self.client.finish()
        pass

    def getresponse(self):
        return self.outputString

    def get_result(self):
        return self.Result

    def onPartialTranscript(self, transcript):
        pass

    def onFinalResponse(self, response):
        print "response: " + str(response)
        string = response["AllResults"][0]["SpokenResponseLong"]
        self.outputString = string
        self.Result = HoundifyResult(response)
        self._active = False

    def onTranslatedResponse(self, response):
        print "Translated response: " + response

    def onError(self, err):
        print "ERROR"

class HoundifyResult(AssistentResult):
    def __init__(self, response):
        if("AllResults" in response):
            allresults = response["AllResults"][0]
            self.Text = allresults["SpokenResponseLong"]
            self.Action = actionMapper[allresults["CommandKind"]]
            if("NativeData" in allresults and "URI" in allresults["NativeData"][0]):
                self.Parameters["url"] = allresults["NativeData"][0]["URI"]

            self.SpokenResponse = allresults["SpokenResponse"]
            self.Hints = allresults["Hints"]
