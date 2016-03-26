import os
import sys
from Conversation.service.flow.engines.personal_assistant.personal_assistent_base import PersonalAssistantBase

__author__ = 'macbook'

try:
    import houndify
    from houndify import HoundListener
except:
    sys.path.append(os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', '..', 'includes', 'houndify')))

    import houndify
    from houndify import HoundListener


clientId = "wniU9od72rVhNhMkbz_CcQ=="
clientKey = "l7onYG8L5ymGmducxBJNke2wDY-m5mPRzCc9Oc8_qNV2MPIheBsKGcaaCpTfxPZDWS-h3AOH_KSagJAsXbF7cg=="

class HoundifyEngine(PersonalAssistantBase, HoundListener):
    def __init__(self, context):
        self.context = context

    def ask_text(self, what):
        print("you said: " + what)

    def open(self):
        self.client = houndify.StreamingHoundClient(clientId, clientKey, sampleRate=8000)
        self.client.setLocation(37.388309, -121.973968)
        self.finished = False
        self.client.start(self)

    def send(self, in_data, frame_count):
        finished = self.client.fill(in_data)

    def close(self):
        self.client.finish()
        pass

    def onPartialTranscript(self, transcript):
        print "Partial transcript: " + transcript

    def onFinalResponse(self, response):
        print "Getting JSON"
        f = open('response.json', 'w')
        string = response["AllResults"][0]["SpokenResponseLong"]
        global outputString
        outputString = string
        global gotAnswer
        gotAnswer = True

    def onTranslatedResponse(self, response):
        print "Translated response: " + response

    def onError(self, err):
        print "ERROR"