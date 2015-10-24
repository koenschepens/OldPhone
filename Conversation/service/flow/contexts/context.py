import ConfigParser
import RPi.GPIO as GPIO
import subprocess
import os
import json
import sys
import tts
from time import sleep
sys.path.insert(0,'..')
import flow

class Context:
    Xbmc = None
    State = None

    def __init__(self, folder):
        self.RootFolder = folder
        self.Config = ConfigParser.RawConfigParser()
        configFile = self.RootFolder + '/conversation.config'
        self.log(configFile)
        self.Config.read(configFile)

        self.Hoorn = self.Config.getint('gpio', 'hook')
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.Hoorn, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    
        sys.path.append(folder)
        import conversation
        sys.path.append(os.path.join(folder, 'kodi'))
        import kodi_container

        self.Conversation = conversation.Conversation()

        self.Language = self.Config.get("settings", "language")
        self.IncludesDir = self.RootFolder + '/includes/'
        self.TtsEngine = tts.tts_pyvona.PyvonaSpeaker(self.Config.get('tts', 'gender'), self.Language) #self.Config.get('settings', 'tts.engine').replace('$includesDir', self.IncludesDir)
        self.SpeechRecognitionEngine = self.IncludesDir + 'speech-recog.sh -l ' + self.Language
        self.PlingCommand = 'aplay -D ' + self.Config.get('settings', 'phonedevice') + ' ' + self.IncludesDir + '/sounds/beepbeep.wav'
        self.TuutCommand = 'aplay -D ' + self.Config.get('settings', 'phonedevice') + ' ' + self.IncludesDir + '/sounds/tuut.wav'

        self.State = flow.initial.Initial(self)


    def run(self):
        self.State.go()

    def isUp(self):
        return GPIO.input(self.Hoorn) == 1;

    def log(self, text):
        print(text)

    def show_notification(self, title, message = ''):
        print(title + ' - ' + message)

    def show_text(self, text):
        print(text)
    
    def getVoiceInput(self, question = None, ringBackTone = True, pling = True):
        if(ringBackTone):
            sleep(1)
            self.executeScript(self.TuutCommand)
            sleep(1)

        if(pling):
            self.executeScript(self.PlingCommand)

        if(question is not None):
            self.say(question)
        
        result = self.executeScript(self.SpeechRecognitionEngine).strip('"')
        
        self.log("result: " + result)

        if(pling):
            self.executeScript(self.PlingCommand)
            
        return result

    def say(self, text):
        self.log("trying to say: '" + text + "' using engine " + str(self.TtsEngine))
        self.TtsEngine.speak(text)
        #subprocess.call([self.TtsEngine, text])

    def executeScript(self, script):
        p = subprocess.Popen(script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        return out

    def ActivateWindow(self, pluginurl = None, window = 'videos'):
        jsonQuery = '{"id":1,"jsonrpc":"2.0","method":"GUI.ActivateWindow","params":{"window":"' + window + '","parameters":["' + pluginurl + '"]}}'
        result = self.get_json_result(jsonQuery)
        return result

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

