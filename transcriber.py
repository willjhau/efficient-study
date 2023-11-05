import whisper

class Transcriber():
    """
    Defines a transcriber object using the OpenAI Whisper library.

    Constructor function has two optional arguments:
        model: the model to use for transcription. Defaults to 'base'.

        language: the language to use for transcription. Defaults to 'en'
    """
    def __init__(self, model='base', language = 'en'):
        self.model = whisper.load_model(model)
        print("model loaded")
        self.language = language
        self.output = None

    # Load a new whisper model
    def loadNewModel(self, model):
        self.model = whisper.load_model(model)
    
    # Change the target language of the model
    def setLanguage(self, lang):
        self.language = lang

    # Transcribe an input file - input requires the file path
    def transcribe(self, file):
        self.output = self.model.transcribe(file, language=self.language)['text']
        return self.output

# Create a testing function with the myrec.wav file
def main():
    model = Transcriber()
    print(model.transcribe('video.mp3'))

if __name__ == '__main__':
    main()