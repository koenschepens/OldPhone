    def play_audio(self, filename):
        try:
            extension = filename.split('.')[1]
        except:
            self.Log("No extension found")

        if(extension == "wav"):
            wf = wave.open(filename, 'rb')

            p = pyaudio.PyAudio()

            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)

            data = wf.readframes(CHUNK)

            while data != '':
                stream.write(data)
                data = wf.readframes(CHUNK)

            stream.stop_stream()
            stream.close()

            p.terminate()