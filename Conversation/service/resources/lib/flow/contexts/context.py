import ConfigParser
import subprocess
import os
import json
import sys
import tts
import pyaudio
import pyglet
from resources.lib import conversation

from time import sleep
#sys.path.insert(0,'..')
#import resources.lib.flow

class Context:
    Xbmc = None
    State = None

    def __init__(self, folderSettings):
        self.FolderSettings = folderSettings
        self._setup()

    def _setup(self):
        self.Config = ConfigParser.RawConfigParser()
        configFile = self.FolderSettings.ConfigFile

        print ("configfile: " + self.FolderSettings.ConfigFile)
        self.log(self.FolderSettings.ConfigFile)
        self.Config.read(self.FolderSettings.ConfigFile)

        import resources.lib.conversation

        self.Language = self.Config.get("settings", "language")
        self.TtsEngine = tts.tts_pyvona.PyvonaSpeaker(self.Config.get('tts', 'gender'), self.Language, self)
        self.SpeechRecognitionEngine = self.FolderSettings.IncludesDir + '/speech-recog.sh -l ' + self.Language
        self.PlingCommand = 'aplay -D ' + self.Config.get('settings', 'phonedevice') + ' ' + self.FolderSettings.IncludesDir + '/sounds/beepbeep.wav'
        self.TuutCommand = 'aplay -D ' + self.Config.get('settings', 'phonedevice') + ' ' + self.FolderSettings.IncludesDir + '/sounds/tuut.wav'
        self.Conversation = conversation.Conversation(self)

    def run(self):
        self.State.handle(None)

    def log(self, text):
        print("[context: context, state: " + self.State.__class__.__name__ + "]: " + text)

    def show_notification(self, title, message = ''):
        print(title + ' - ' + message)

    def show_text(self, text):
        print(text)

    def play_audio(self, filename):
        try:
            extension = filename.split('.')[1]
        except:
            self.Log("No extension found")

        if(extension == "wav"):
            wf = wave.open(filename, 'rb')

            p = pyaudio.PyAudio()

            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)

            data = wf.readframes(CHUNK)

            while data != '':
                stream.write(data)
                data = wf.readframes(CHUNK)

            stream.stop_stream()
            stream.close()

            p.terminate()
        elif(extension == "mp3"):
            self.executeScript("mplayer " + filename + " -ao alsa:device=hw=1,1")
    
    def getVoiceInput(self, question = None, ringBackTone = False, pling = False):
        if(ringBackTone):
            sleep(1)
            self.executeScript(self.TuutCommand)
            sleep(1)

        if(question is not None):
            self.say(question)
        
        if(pling):
            self.executeScript(self.PlingCommand)

        self.log("Using speech engine: " + self.SpeechRecognitionEngine)

        result = self.executeScript(self.SpeechRecognitionEngine)

        if(result is not None):
            result = result.strip('"')
        
        self.log("result: " + result)

        if(pling):
            self.executeScript(self.PlingCommand)
            
        return result

    def say(self, text):
        self.log("saying: '" + text + "' using engine " + str(self.TtsEngine))
        self.TtsEngine.speak(text)
        #subprocess.call([self.TtsEngine, text])

    def executeScript(self, script):
        p = subprocess.Popen(script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        p.wait()
        return out

    def ActivateWindow(self, pluginurl = None, window = 'videos'):
        jsonQuery = '{"id":1,"jsonrpc":"2.0","method":"GUI.ActivateWindow","params":{"window":"' + window + '","parameters":["' + pluginurl + '"]}}'
        result = self.get_json_result(jsonQuery)
        return result

    def send_input_to_client(self, text):
        jsonQuery = '{"id":1,"jsonrpc":"2.0","method":"Input.SendText","params":{"text":"' + text + '"}}'
        self.log(jsonQuery)
        jsonResponse = self.get_json_result(jsonQuery)
        self.log(jsonResponse)
        return jsonResponse

    def get_json_result(self, query):
        return json.loads('{"status" : {"code":"200"}}')
        
    def search_youtube(self, query):
        script = self.IncludesDir + 'youtube-search ' + query

        self.log("searching youtube with script'" + script + "'")
        
        p = subprocess.Popen(script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        youtubeId, err = p.communicate()

        return youtubeId

    def Player_Open(self, url):
        action = 'Player.Open(' + url + ')'
        self.send_action(action)

    def send_action(self, action):
        self.log("Send action: " + action)

    def userInputRequired(self):
        return True

