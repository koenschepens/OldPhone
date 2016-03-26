import struct
import math
import wave
import pyaudio
import time
from Conversation.service.flow.engines.sound.sound_base import SoundBase

INITIAL_VOL_THRESHOLD = 0.010
FORMAT = pyaudio.paInt16
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 1
RATE = 44100
CHUNK = 1024
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
# if we get this many noisy blocks in a row, increase the threshold
OVERSENSITIVE = 15.0/INPUT_BLOCK_TIME
# if we get this many quiet blocks in a row, decrease the threshold
UNDERSENSITIVE = 120.0/INPUT_BLOCK_TIME

__author__ = 'macbook'
class AudioInOut(SoundBase):
    def play_dial_tone(self, output):
        self.context.execute_script('aplay -D ' + self.context.config.get('output', output) + ' ' + self.context.includes_dir + '/sounds/beepbeep.wav')

    def play_beep(self, output):
        self.context.execute_script('aplay -D ' + self.context.config.get('output', output) + ' ' + self.context.includes_dir + '/sounds/tuut.wav')

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

    def find_output_device(self):
        device_index = None
        for i in range( self.pa.get_device_count() ):
            devinfo = self.pa.get_device_info_by_index(i)
            print( "Device %d: %s"%(i,devinfo["name"]) )

            for keyword in ["output","out"]:
                if keyword in devinfo["name"].lower():
                    print( "Found an output: device %d - %s"%(i,devinfo["name"]) )
                    device_index = i
                    return device_index

        if device_index == None:
            print( "No preferred input found; using default input device." )

        return device_index

    def open(self):
        self.pa = pyaudio.PyAudio()
        self.input_device_index = self.find_input_device()
        self.output_device_index = self.find_output_device()

    def close(self):
        self.pa.terminate()

    def play_wav(self, path):
        wf = wave.open(path, 'rb')

        self.output_stream = self.pa.open(format = FORMAT,
                             channels = CHANNELS,
                             rate = RATE,
                             input = False,
                             output=True,
                             output_device_index=self.output_device_index,
                             frames_per_buffer = INPUT_FRAMES_PER_BLOCK)

        # read data (based on the chunk size)
        data = wf.readframes(CHUNK)

        # play stream (looping from beginning of file to the end)
        while data != '':
            # writing to the stream is what *actually* plays the sound.
            self.output_stream.write(data)
            data = wf.readframes(CHUNK)

        # cleanup stuff.
        self.output_stream.close()
        self.pa.terminate()

    def play_ogg(self, path):
        import pygame
        pygame.init()
        song = pygame.mixer.Sound(path)
        clock = pygame.time.Clock()
        song.play()
        while True:
            clock.tick(60)
        pygame.quit()

    def record(self, assistant_callback):
        self.silentcount = 0
        self.startedTalking = False

        def callback(in_data, frame_count, time_info, status):
            amplitude = self.get_rms(in_data)
            assistant_callback(in_data, frame_count)

            if(not self.startedTalking and amplitude > INITIAL_VOL_THRESHOLD):
                self.startedTalking = True
                self.context.log("started talking...")

            if(self.startedTalking):
                if(amplitude <= INITIAL_VOL_THRESHOLD):
                    self.silentcount += 1
                else:
                    self.silentcount = 0

                assistant_callback(in_data, frame_count)

                if(self.silentcount > int(self.context.config.get("sound", "wait_after_speak"))):
                    self.context.log("stopped talking...")
                    return (in_data, pyaudio.paComplete)

            return (in_data, pyaudio.paContinue)

        self.input_stream = self.pa.open(format = FORMAT,
                             channels = CHANNELS,
                             rate = RATE,
                             input = True,
                             input_device_index = self.input_device_index,
                             frames_per_buffer = INPUT_FRAMES_PER_BLOCK,
                             stream_callback = callback)

        self.input_stream.start_stream()

        while self.input_stream.is_active():
                time.sleep(0.1)

        self.input_stream.stop_stream()
        self.input_stream.close()
        self.startedTalking = False
        self.silentcount = 0
