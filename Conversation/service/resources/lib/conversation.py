import os.path, sys
import json
import struct
import pyaudio
import ConfigParser
import re
import math

INITIAL_VOL_THRESHOLD = 0.010
FORMAT = pyaudio.paInt16
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 1
RATE = 16000
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
# if we get this many noisy blocks in a row, increase the threshold
OVERSENSITIVE = 15.0/INPUT_BLOCK_TIME
# if we get this many quiet blocks in a row, decrease the threshold
UNDERSENSITIVE = 120.0/INPUT_BLOCK_TIME
# if the noise was longer than this many blocks, it's not a 'tap'
MAX_TAP_BLOCKS = 0.15/INPUT_BLOCK_TIME

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

class Conversation:
    def __init__(self):
        self.client_access_token = client_access_token
        self.subscription_key = subscription_key
        self.Api = apiai.ApiAI(self.client_access_token, self.subscription_key)

    def get_rms(self, block):
        # RMS amplitude is defined as the square root of the
        # mean over time of the square of the amplitude.
        # so we need to convert this string of bytes into
        # a string of 16-bit samples...

        # we will get one short out for each
        # two chars in the string.
        count = len(block)/2
        format = "%dh"%(count)
        shorts = struct.unpack( format, block )

        # iterate over the block.
        sum_squares = 0.0
        for sample in shorts:
            # sample is a signed short in +/- 32768.
            # normalize it to 1.0
            n = sample * SHORT_NORMALIZE
            sum_squares += n*n

        return math.sqrt( sum_squares / count )

    def ask_speech(self):
        self.pa = pyaudio.PyAudio()
        self.stream = self.open_mic_stream()

        ''' voice_request = ai.text_request()
            bytessize = 2048

            with open('log.raw', 'rb') as f:
                data = f.read(bytessize)
                while data:
                    request.send(data)
                    data = f.read(bytessize)

         request.getresponse() '''

        voice_request = self.Api.voice_request()

        silentcount = 0

        BUFFER_SIZE = 2048
        samples = self.stream.read(BUFFER_SIZE, exception_on_overflow = False)
        amplitude = self.get_rms(samples)

        while(amplitude <= INITIAL_VOL_THRESHOLD):
            samples = self.stream.read(BUFFER_SIZE, exception_on_overflow = False)
            amplitude = self.get_rms(samples)
            print("_amp: %s" % amplitude)

        print("you're talking now!")

        run = True

        while(run):
            if(amplitude <= INITIAL_VOL_THRESHOLD):
                silentcount += 1
            else:
                silentcount = 0

            print("amp: %s" % amplitude)
            voice_request.send(samples)
            samples = self.stream.read(BUFFER_SIZE, exception_on_overflow = False)
            amplitude = self.get_rms(samples)

            if(silentcount > 10):
                run = False

        voice_request.send(samples)
        print("stopped talking...")

        response = voice_request.getresponse()
        leJson = response.read()
        parsed_json = json.loads(leJson)

        self.Result = Result(parsed_json, self.client_access_token, self.subscription_key)

        return self.Result

    def ask_text(self, what):
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

    def find_input_device(self):
        device_index = None
        for i in range( self.pa.get_device_count() ):
            devinfo = self.pa.get_device_info_by_index(i)
            print( "Device %d: %s"%(i,devinfo["name"]) )

            for keyword in ["mic","input"]:
                if keyword in devinfo["name"].lower():
                    print( "Found an input: device %d - %s"%(i,devinfo["name"]) )
                    device_index = i
                    return device_index

        if device_index == None:
            print( "No preferred input found; using default input device." )

        return device_index

    def open_mic_stream(self):
        device_index = self.find_input_device()

        stream = self.pa.open(   format = FORMAT,
                                 channels = CHANNELS,
                                 rate = RATE,
                                 input = True,
                                 input_device_index = device_index,
                                 frames_per_buffer = INPUT_FRAMES_PER_BLOCK)

        return stream


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