import json
import os
import re
import sys
from service.flow.engines.personal_assistant.personal_assistent_base import PersonalAssistantBase, AssistentResult, ImmediateResult

RATE = 44100

try:
    import apiai
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
    import apiai
__author__ = 'macbook'

class ApiAi(PersonalAssistantBase):
    def __init__(self, context):
        PersonalAssistantBase.__init__(self, context)
        self.client_access_token = context.config.get('aiapi', 'client_access_token')
        self.subscription_key = context.config.get('aiapi', 'subscription_key')

        self.Api = apiai.ApiAI(self.client_access_token, self.subscription_key)

    def ask_text(self, what):
        if(len(what) == 0):
            self.Result = AssistentResult("Sorry, I didn't hear you")
            return self.Result

        self.Request = what
        immediateActions = self.context.config.options("immediateActions")

        if(self.Request in immediateActions):
            configValue = self.context.config.get("immediateActions", self.Request)

            action = re.search('(\w*)\((\w*)\)', configValue)
            method_name = action.group(1)
            params = action.group(2)
            immediateResult = ImmediateResult()
            method = getattr(ImmediateResult, method_name)
            if not method:
                raise Exception("Method %s not implemented" % method_name)

            return method(immediateResult, params)

        request = self.Api.text_request()

        request.query = what
        response = request.getresponse()
        leJson = response.read()

        parsed_json = json.loads(leJson)

        self.Result = AssistentResult(parsed_json, self.client_access_token, self.subscription_key)

        return self.Result

    def open(self):
        self.vad = apiai.VAD()
        self.resampler = apiai.Resampler(source_samplerate=RATE)

        self.request = self.Api.voice_request()
        self.request.lang = 'en' # optional, default value equal 'en'

    def send(self, in_data, frame_count):
        frames, data = self.resampler.resample(in_data, frame_count)
        state = self.vad.processFrame(frames)
        self.request.send(data)

        return data, state

    def close(self):
        pass

class ApiAiResult(AssistentResult):
    def __init__(self, parsed_json):
        self.Id = 1000
        self.NextFunction = None
        self.NeedsUserInput = False
        self.Action = {}
        self.IncludesDir = os.path.dirname(os.path.realpath(__file__)) + '/includes/'
        self.ResolvedQuery = parsed_json

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
