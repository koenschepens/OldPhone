
import os.path, sys
import json
import subprocess 


try:
    import apiai
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
    import apiai

import time
import scipy.io.wavfile as wav

includesDir = os.path.dirname(os.path.realpath(__file__)) + '/includes/'

class Conversation:
    def __init__(self, client_access_token, subscription_key):
        self.client_access_token = client_access_token
        self.subscription_key = subscription_key
        
    def ask(self, what):
        ai = apiai.ApiAI(self.client_access_token, self.subscription_key)
        request = ai.text_request()
        request.query = what
        response = request.getresponse()
        leJson = response.read()
        print (leJson)
        parsed_json = json.loads(leJson)

        result = Result(parsed_json)
        print(result.getKodiAction())

class Result:
    def __init__(self, parsed_json):
        self.Text = parsed_json['result']['fulfillment']['speech']
        self.Action = parsed_json['result']['action']
        if('parameters' in parsed_json):
            self.Parameters = parsed_json['result']['parameters']

    def getKodiAction(self):
        actions = {
            'weather.search': self.weather,
            'media.video_play': self.video_play,
            'entertainment.songs': self.songs
        }
        func = actions.get(self.Action, lambda: "nothing")
        return func()

    def songs(self):
         #if('q' in self.Parameters):
         return self.get_activatewindow_json("music", 501)

    def video_play(self):
        services = {
            'youtube': self.video_play_youtube,
            'movie' : self.video_play_popcorn_time
        }

        if('service_name' in self.Parameters):
            func = services.get(self.Parameters['service_name'], lambda: None)
            return func()
        else:
            return self.video_play_popcorn_time()

    def weather(self):
        return self.Text

    def video_play_popcorn_time(self):
        if(self.Parameters['q'] is None):
            return self.get_addon_json('plugin.video.kodipopcorntime', '{  }')
        else:        
            return self.get_addon_json('plugin.video.kodipopcorntime', '"search": "' + self.Parameters['q'] + '"')

    def get_addon_json(self, addonid, params):
        return '{ "jsonrpc": "2.0", "method": "Addons.ExecuteAddon", "params": { "wait": false, "addonid": "' + addonid + '", "params": { ' + params + ' } }, "id": 2 }'

    def get_activatewindow_json(self, window, id):
        return '{ "jsonrpc": "2.0", "method": "GUI.ActivateWindow", "params": { "window": "' + window + '" }, "id": ' + str(id) + ' }'

    def video_play_youtube(self):
        global includesDir
        if(self.Parameters['q'] is None):
            self.LastMethod = self.video_play_youtube
            return "Nothing found"
        else:
            script = includesDir + 'youtube-search ' + self.Parameters['q']
            print(script)
            p = subprocess.Popen(script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            youtubeId, err = p.communicate()
            return '{"id":1,"jsonrpc":"2.0","method":"Player.Open","params":{"item":{"file":"plugin:\/\/plugin.video.youtube\/?path=\/root\/search&action=play_video&videoid=' + youtubeId + '"}}}'    

#tokens = { 'dutch' : 'b240ec13475a464890af46b48f49f5c7', 'english' : 'fb928615eb914f4785e110eecad49c95' }

#language = sys.argv[1]
#text = sys.argv[2]

#conversation = Conversation(tokens[language], '7c4c06c1-eb1d-4fd3-9367-134f20cbcb25')

#conversation.ask(text)