import sys

import subprocess
import json

sys.path.insert(0,'..')

class TargetBase:
    context = None

    def __init__(self, context):
        self.context = context

    def isUp(self):
        pass

    def log(self, text):
        print(text)

    def show_notification(self, title, message = ''):
        print(title + ' - ' + message)

    def show_text(self, text):
        print(text)

    def execute_script(self, script):
        p = subprocess.Popen(script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        return out

    def activate_window(self, pluginurl = None, window = 'videos'):
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

    def player_open(self, url):
        action = 'Player.Open(' + url + ')'
        self.send_action(action)

    def send_action(self, action):
        self.log("Send action: " + action)

    def user_input_required(self):
        return True

    def search_movie(self, query):
        url = 'plugin://plugin.video.kodipopcorntime/search?query=' + query + ''
        self.activate_window(url, window='videos')

    def search_genre(self, genre):
        if(genre is not None):
            url = 'plugin://plugin.video.kodipopcorntime/genres/' + genre + '/1?limit=20'
        else:
            url = "plugin://plugin.video.kodipopcorntime/genres"

        self.activate_window(url, window='videos')