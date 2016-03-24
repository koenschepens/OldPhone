__author__ = 'macbook'

import sys
import os
import pyaudio

INITIAL_TAP_THRESHOLD = 0.010
FORMAT = pyaudio.paInt16
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 2
RATE = 48000
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
# if we get this many noisy blocks in a row, increase the threshold
OVERSENSITIVE = 15.0/INPUT_BLOCK_TIME
# if we get this many quiet blocks in a row, decrease the threshold
UNDERSENSITIVE = 120.0/INPUT_BLOCK_TIME
# if the noise was longer than this many blocks, it's not a 'tap'
MAX_TAP_BLOCKS = 0.15/INPUT_BLOCK_TIME

try:
    import houndify

except:
    sys.path.append(os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', '..', 'includes', 'houndify')))
    import houndify as houndify

class SpeechRecognition():
    def __init__(self, context):
        self.pa = pyaudio.PyAudio()
        self.Language = context.Language
        self.IncludesDir = context.IncludesDir
        self.Context = context

    def get(self):
        self.stream = self.open_mic_stream()

        CLIENT_ID = "wniU9od72rVhNhMkbz_CcQ=="
        CLIENT_KEY = "l7onYG8L5ymGmducxBJNke2wDY-m5mPRzCc9Oc8_qNV2MPIheBsKGcaaCpTfxPZDWS-h3AOH_KSagJAsXbF7cg=="

        #
        # Simplest HoundListener; just print out what we receive.
        #
        # You can use these callbacks to interact with your UI.
        #
        class MyListener(houndify.HoundListener):
            def onPartialTranscript(self, transcript):
                print "Partial transcript: " + transcript
            def onFinalResponse(self, response):
                print "Final response: " + str(response)
            def onTranslatedResponse(self, response):
                print "Translated response: " + response
            def onError(self, err):
                print "ERROR"

        client = houndify.StreamingHoundClient(CLIENT_ID, CLIENT_KEY)
        ## Pretend we're at SoundHound HQ.  Set other fields as appropriate
        client.setLocation(37.388309, -121.973968)

        BUFFER_SIZE = 512
        samples = self.stream.read(BUFFER_SIZE, exception_on_overflow = False)
        #samples = sys.stdin.read(BUFFER_SIZE)
        finished = False
        client.start(MyListener())
        while not finished:
            finished = client.fill(samples)
            samples = sys.stdin.read(BUFFER_SIZE)
            if len(samples) == 0:
                break
        client.finish()

    def listen(self):
        try:
            block = self.stream.read(INPUT_FRAMES_PER_BLOCK)
        except IOError, e:
            # dammit.
            self.errorcount += 1
            print( "(%d) Error recording: %s"%(self.errorcount,e) )
            self.noisycount = 1
            return


    def stop(self):
        self.stream.close()

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

    def open_mic_stream( self ):
        device_index = self.find_input_device()

        stream = self.pa.open(   format = FORMAT,
                                 channels = CHANNELS,
                                 rate = RATE,
                                 input = True,
                                 input_device_index = device_index,
                                 frames_per_buffer = INPUT_FRAMES_PER_BLOCK)

        return stream
