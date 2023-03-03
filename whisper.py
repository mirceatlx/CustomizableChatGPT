import openai

class Whisper:
    def __init__(self, key):
        self.key = key
        openai.api_key = self.key
    
    def transcribe(self, audio_file):
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript['text']