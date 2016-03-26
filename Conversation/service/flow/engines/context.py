import os
import sys
from time import sleep
from Conversation.service.flow.engines.personal_assistant.personal_assistent_base import Result
from Conversation.service.flow.states.initial import Initial

class Context():
    target_engine = None
    tts_engine = None
    speech_recognition_engine = None
    personal_assistant = None
    input_engine = None
    sound_engine = None
    config = None
    language = None
    state = None

    def __init__(self, config, root_folder, includes_dir, language):
        self.root_folder = root_folder
        self.includes_dir = includes_dir
        self.language = language
        self.config = config
        sys.path.append(root_folder)
        sys.path.append(os.path.join(self.root_folder, 'target'))
        self.state = Initial(self)

    def log(self, message):
        if(self.target_engine is not None):
            self.target_engine.log(message)
        else:
            print(message)

    def isUp(self):
        return self.input_engine.isUp()

    def run(self):
        self.state.go()

    def ask(self, message = None):
        if(message is None):
            self.sound_engine.open()

            self.personal_assistant.open()

            def callback(in_data, frame_count):
                self.personal_assistant.send(in_data, frame_count)

            self.sound_engine.record(callback)

            self.sound_engine.close()
            self.personal_assistant.close()

        json = self.personal_assistant.get_json_response()

        self.log(json)

        self.Result = Result(json)

        return self.Result

    def say(self, message):
        self.tts_engine.speak(message, self.sound_engine)

    def show_notification(self, title, message = ''):
        self.target_engine.show_notification(title, message)

    def user_input_required(self):
        return self.target_engine.user_input_required()

    def play_movie(self, result):
        params = result.Parameters
        if('title' in params and params['title'] != '$title'):
            q = params['title']
            self.target_engine.search_movie(q)
            url = 'plugin://plugin.video.kodipopcorntime/search?query=' + q + ''
        elif('searchQuery' in params and params['searchQuery'] != '$q'):
            q = params['searchQuery']
            url = 'plugin://plugin.video.kodipopcorntime/search?query=' + q + ''
        elif('genre' in params and params['genre'] != '$genre'):
            url = 'plugin://plugin.video.kodipopcorntime/genres/' + params['genre'] + '/1?limit=20'
        else:
            url = "plugin://plugin.video.kodipopcorntime/genres"

        container = self.context.activate_window(url, window='videos')

    def show_weather(self, result):
        self.target_engine.activate_window(pluginurl = None, window = "weather")

    def send_action(self, action):
        self.target_engine.send_action(action)