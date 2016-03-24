import pyvona
import speaker
import sys
import json
import os
import string

class PyvonaSpeaker(speaker.Speaker):
    def __init__(self, gender, language, context):
        self.Context = context
        speaker.Speaker.__init__(self, gender, language)
        self.Pyvona = pyvona.create_voice("GDNAIRN4SS66PRNKPQZQ","2gURBTiaqnkjxEXZX+cslGhkJ+OVKTzWCZg7mvpp")
        self.Pyvona.codec = "mp3"
        allVoices = self.Pyvona.list_voices()
        self.DesiredVoice = "Ruben"
        for voice in allVoices["Voices"]:
            if(voice["Gender"] == gender and voice["Language"].lower().startswith(language)):
                self.DesiredVoice = voice["Name"]
                pass
        self.Pyvona.voice_name = self.DesiredVoice
        
        self.VoiceDir = os.path.join(self.Context.FolderSettings.IncludesDir, "voices", "pyvona", language, self.DesiredVoice)
        if not os.path.exists(self.VoiceDir):
            os.makedirs(self.VoiceDir)
        pygame.init()

    def speak(self, text):
        try:
            filename = os.path.join(self.VoiceDir, self.format_filename(text + "." + self.Pyvona.codec))
            if(not os.path.exists(filename)):
                self.Context.log("writing to file " + filename + "...")
                self.Pyvona.fetch_voice(text, filename)
                self.Context.log("done writing to file")

            self.Context.play_audio(filename)
            """if(not pygame.mixer.get_init()):
                pygame.mixer.init()
            #pygame.mixer.music.load(filename)
            channel = pygame.mixer.Channel(6)
            sound = pygame.mixer.Sound(filename)
            channel.play(sound)
            while channel.get_busy():
                pass"""

        except pyvona.PyvonaException as e:
            self.Context.log("couldn't fetch voice to dir " + self.VoiceDir + ". Error was: " + str(e))
            self.Pyvona.speak(text)

    def format_filename(self, s):
        """Take a string and return a valid filename constructed from the string.
        Uses a whitelist approach: any characters not present in valid_chars are
        removed. Also spaces are replaced with underscores.
         
        Note: this method may produce invalid filenames such as ``, `.` or `..`
        When I use this method I prepend a date string like '2009_01_15_19_46_32_'
        and append a file extension like '.txt', so I avoid the potential of using
        an invalid filename.
         
        """
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        filename = ''.join(c for c in s if c in valid_chars)
        filename = filename.replace(' ','_') # I don't like spaces in filenames.
        return filename

"""'{"Voices":[{"Gender":"Female","Language":"en-US","Name":"Salli"},{"Gender":"Male","Language":"en-US","Name":"Joey"},{"Gender":"Female","Language":"da-DK","Name":"Naja"},{"Gender":"Male","Language":"da-DK","Name":"Mads"},{"Gender":"Female","Language":"de-DE","Name":"Marlene"},{"Gender":"Male","Language":"de-DE","Name":"Hans"},{"Gender":"Female","Language":"en-AU","Name":"Nicole"},{"Gender":"Male","Language":"en-AU","Name":"Russell"},{"Gender":"Female","Language":"en-GB","Name":"Amy"},{"Gender":"Male","Language":"en-GB","Name":"Brian"},{"Gender":"Female","Language":"en-GB","Name":"Emma"},{"Gender":"Female","Language":"en-GB-WLS","Name":"Gwyneth"},{"Gender":"Male","Language":"en-GB-WLS","Name":"Geraint"},{"Gender":"Female","Language":"cy-GB","Name":"Gwyneth"},{"Gender":"Male","Language":"cy-GB","Name":"Geraint"},{"Gender":"Female","Language":"en-IN","Name":"Raveena"},{"Gender":"Male","Language":"en-US","Name":"Chipmunk"},{"Gender":"Male","Language":"en-US","Name":"Eric"},{"Gender":"Female","Language":"en-US","Name":"Ivy"},{"Gender":"Female","Language":"en-US","Name":"Jennifer"},{"Gender":"Male","Language":"en-US","Name":"Justin"},{"Gender":"Female","Language":"en-US","Name":"Kendra"},{"Gender":"Female","Language":"en-US","Name":"Kimberly"},{"Gender":"Female","Language":"es-ES","Name":"Conchita"},{"Gender":"Male","Language":"es-ES","Name":"Enrique"},{"Gender":"Female","Language":"es-US","Name":"Penelope"},{"Gender":"Male","Language":"es-US","Name":"Miguel"},{"Gender":"Female","Language":"fr-CA","Name":"Chantal"},{"Gender":"Female","Language":"fr-FR","Name":"Celine"},{"Gender":"Male","Language":"fr-FR","Name":"Mathieu"},{"Gender":"Female","Language":"is-IS","Name":"Dora"},{"Gender":"Male","Language":"is-IS","Name":"Karl"},{"Gender":"Female","Language":"it-IT","Name":"Carla"},{"Gender":"Male","Language":"it-IT","Name":"Giorgio"},{"Gender":"Female","Language":"nb-NO","Name":"Liv"},{"Gender":"Female","Language":"nl-NL","Name":"Lotte"},{"Gender":"Male","Language":"nl-NL","Name":"Ruben"},{"Gender":"Female","Language":"pl-PL","Name":"Agnieszka"},{"Gender":"Male","Language":"pl-PL","Name":"Jacek"},{"Gender":"Female","Language":"pl-PL","Name":"Ewa"},{"Gender":"Male","Language":"pl-PL","Name":"Jan"},{"Gender":"Female","Language":"pl-PL","Name":"Maja"},{"Gender":"Female","Language":"pt-BR","Name":"Vitoria"},{"Gender":"Male","Language":"pt-BR","Name":"Ricardo"},{"Gender":"Male","Language":"pt-PT","Name":"Cristiano"},{"Gender":"Female","Language":"pt-PT","Name":"Ines"},{"Gender":"Female","Language":"ro-RO","Name":"Carmen"},{"Gender":"Male","Language":"ru-RU","Name":"Maxim"},{"Gender":"Female","Language":"ru-RU","Name":"Tatyana"},{"Gender":"Female","Language":"sv-SE","Name":"Astrid"},{"Gender":"Female","Language":"tr-TR","Name":"Filiz"}]}'"""