from dotenv import load_dotenv
from chat import ChatBot
from personalities import *
from modules import *
from discord_bot import DiscordBot
from whisper import Whisper
import os

load_dotenv()

DISCORD_KEY = os.getenv("DISCORD_KEY")
OPENAI_KEY = os.getenv("OPENAI_KEY")
PORCUPINE = os.getenv("PORCUPINE")

print(DISCORD_KEY)
# Create a new ChatBot instance
chatbot = ChatBot(
    personality=WaldiePersonality(),
    modules=[
        WebSearchModule(),
    ],
    ignore_warnings=True,
    key = OPENAI_KEY
)

# Whisper
whisper = Whisper(OPENAI_KEY)

# Run the discord bot
discord_bot = DiscordBot(chatbot, DISCORD_KEY)

discord_bot.run()

import pyaudio
import wave

def speak(text):
    from win32com.client import Dispatch
    speak = Dispatch("SAPI.SpVoice")
    speak.Speak(text)

def output_file_recording():


    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def listen_for_5_seconds():

    output_file_recording()

    # listen for 5 seconds using the microphone with pyaudio
    audio_file = open('output.wav', "rb")

    # Transcribe the audio file
    transcript = whisper.transcribe(audio_file)

    speak(chatbot.answer(transcript))    

import struct
import pyaudio
import pvporcupine

porcupine = None
pa = None
audio_stream = None

try:
    porcupine = pvporcupine.create(keywords=["computer", "jarvis"], access_key=PORCUPINE)

    pa = pyaudio.PyAudio()

    audio_stream = pa.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=porcupine.frame_length)

    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)

        if keyword_index >= 0:
            listen_for_5_seconds()
            speak("Computer online")
except Exception as e:
    print("somethignwent wrong")
    print(e)