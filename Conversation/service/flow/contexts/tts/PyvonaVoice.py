import tempfile
import pyvona
from tempfile import NamedTemporaryFile
import subprocess

__author__ = 'macbook'

class PyvonaVoice(pyvona.Voice):

    def speak(self, text_to_speak):
        """Speak a given text
        """
        with NamedTemporaryFile(delete=True) as f:
            subprocess.call(["mplayer", f.name])
