import subprocess

__author__ = 'macbook'

key = "f914bec79b1941d2ac773bdce38cd4e9"

class Voicerss():
    def __init__(self, gender, language):
        self.Gender = gender
        self.language = language

    def speak(voice, text):
        url = "https://api.voicerss.org/?key=%s&src=%s" % (key, text)
        subprocess.call("mplayer", "-ao", "alsa:plughw:1:0", url)