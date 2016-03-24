import os
import pyvona
import subprocess
import tempfile

__author__ = 'macbook'

class PyvonaVoice(pyvona.Voice):
    def speak(self, text_to_speak):
        """Speak a given text
        """

        path = os.path.join(tempfile.gettempdir(), text_to_speak + ".wav")

        if(not os.path.exists(path)):
            with open(path, mode = 'w+') as f:
                with self.use_ogg_codec():
                    self.fetch_voice_fp(text_to_speak, f)

        print(path)
        subprocess.call(["mplayer", path])
