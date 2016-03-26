import os
import tempfile

import pyvona
import speaker

class TtsPyvona(speaker.Speaker):
    def __init__(self, context, gender, language):
        speaker.Speaker.__init__(self, gender, language)
        self.pyvona_voice = self.create_voice("GDNAIRN4SS66PRNKPQZQ","2gURBTiaqnkjxEXZX+cslGhkJ+OVKTzWCZg7mvpp")
        allVoices = self.pyvona_voice.list_voices()
        self.DesiredVoice = "Ruben"
        for voice in allVoices["Voices"]:
            if(voice["Gender"] == gender and voice["Language"] == language):
                self.DesiredVoice = voice["Name"]
                pass
        self.pyvona_voice.voice_name = self.DesiredVoice

    def speak(self, text, sound_engine):
        self.pyvona_voice.speak(text, sound_engine)

    def create_voice(self, access_key, secret_key):
        """Creates and returns a voice object to interact with
        """
        return Pyvona_voice(access_key, secret_key)

class Pyvona_voice(pyvona.Voice):
    def speak(self, text_to_speak, sound_engine):
        """Speak a given text
        """
        path = os.path.join(tempfile.gettempdir(), text_to_speak + ".ogg")

        if(not os.path.exists(path)):
            with open(path, mode = 'w+') as f:
                with self.use_ogg_codec():
                    self.fetch_voice_fp(text_to_speak, f)

        print(path)
        #subprocess.call(["mplayer", path, "-ao", hwout])
        sound_engine.play_ogg(path)

class Pyvona():
    def speak(lang, text):
        args = text
        v = pyvona.create_voice("GDNAIRN4SS66PRNKPQZQ","2gURBTiaqnkjxEXZX+cslGhkJ+OVKTzWCZg7mvpp")
        #v.voice_name="Ruben"
        v.speak(args)

"""'{"Voices":[{"Gender":"Female","Language":"en-US","Name":"Salli"},{"Gender":"Male","Language":"en-US","Name":"Joey"},{"Gender":"Female","Language":"da-DK","Name":"Naja"},{"Gender":"Male","Language":"da-DK","Name":"Mads"},{"Gender":"Female","Language":"de-DE","Name":"Marlene"},{"Gender":"Male","Language":"de-DE","Name":"Hans"},{"Gender":"Female","Language":"en-AU","Name":"Nicole"},{"Gender":"Male","Language":"en-AU","Name":"Russell"},{"Gender":"Female","Language":"en-GB","Name":"Amy"},{"Gender":"Male","Language":"en-GB","Name":"Brian"},{"Gender":"Female","Language":"en-GB","Name":"Emma"},{"Gender":"Female","Language":"en-GB-WLS","Name":"Gwyneth"},{"Gender":"Male","Language":"en-GB-WLS","Name":"Geraint"},{"Gender":"Female","Language":"cy-GB","Name":"Gwyneth"},{"Gender":"Male","Language":"cy-GB","Name":"Geraint"},{"Gender":"Female","Language":"en-IN","Name":"Raveena"},{"Gender":"Male","Language":"en-US","Name":"Chipmunk"},{"Gender":"Male","Language":"en-US","Name":"Eric"},{"Gender":"Female","Language":"en-US","Name":"Ivy"},{"Gender":"Female","Language":"en-US","Name":"Jennifer"},{"Gender":"Male","Language":"en-US","Name":"Justin"},{"Gender":"Female","Language":"en-US","Name":"Kendra"},{"Gender":"Female","Language":"en-US","Name":"Kimberly"},{"Gender":"Female","Language":"es-ES","Name":"Conchita"},{"Gender":"Male","Language":"es-ES","Name":"Enrique"},{"Gender":"Female","Language":"es-US","Name":"Penelope"},{"Gender":"Male","Language":"es-US","Name":"Miguel"},{"Gender":"Female","Language":"fr-CA","Name":"Chantal"},{"Gender":"Female","Language":"fr-FR","Name":"Celine"},{"Gender":"Male","Language":"fr-FR","Name":"Mathieu"},{"Gender":"Female","Language":"is-IS","Name":"Dora"},{"Gender":"Male","Language":"is-IS","Name":"Karl"},{"Gender":"Female","Language":"it-IT","Name":"Carla"},{"Gender":"Male","Language":"it-IT","Name":"Giorgio"},{"Gender":"Female","Language":"nb-NO","Name":"Liv"},{"Gender":"Female","Language":"nl-NL","Name":"Lotte"},{"Gender":"Male","Language":"nl-NL","Name":"Ruben"},{"Gender":"Female","Language":"pl-PL","Name":"Agnieszka"},{"Gender":"Male","Language":"pl-PL","Name":"Jacek"},{"Gender":"Female","Language":"pl-PL","Name":"Ewa"},{"Gender":"Male","Language":"pl-PL","Name":"Jan"},{"Gender":"Female","Language":"pl-PL","Name":"Maja"},{"Gender":"Female","Language":"pt-BR","Name":"Vitoria"},{"Gender":"Male","Language":"pt-BR","Name":"Ricardo"},{"Gender":"Male","Language":"pt-PT","Name":"Cristiano"},{"Gender":"Female","Language":"pt-PT","Name":"Ines"},{"Gender":"Female","Language":"ro-RO","Name":"Carmen"},{"Gender":"Male","Language":"ru-RU","Name":"Maxim"},{"Gender":"Female","Language":"ru-RU","Name":"Tatyana"},{"Gender":"Female","Language":"sv-SE","Name":"Astrid"},{"Gender":"Female","Language":"tr-TR","Name":"Filiz"}]}'"""