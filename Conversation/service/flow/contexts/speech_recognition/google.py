__author__ = 'macbook'

class SpeechRecognition():
    def __init__(self, context):
        self.Language = context.Language
        self.IncludesDir = context.IncludesDir
        self.Context = context

    def get(self):
        return self.Context.executeScript(self.IncludesDir + 'speech-recog.sh -l ' + self.Language).strip('"')
