import pyaudio
import wave

import io
import os
import sounddevice as sd
import numpy as np

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

import aubio
import numpy as num
import pyaudio
import sys

# Some constants for setting the PyAudio and the
# Aubio.
BUFFER_SIZE             = 2048
CHANNELS                = 1
FORMAT                  = pyaudio.paFloat32
METHOD                  = "default"
SAMPLE_RATE             = 44100
HOP_SIZE                = BUFFER_SIZE//2
PERIOD_SIZE_IN_FRAME    = HOP_SIZE



# Initiating PyAudio object.
pA = pyaudio.PyAudio()
# Open the microphone stream.
mic = pA.open(format=FORMAT, channels=CHANNELS,
    rate=SAMPLE_RATE, input=True,
    frames_per_buffer=PERIOD_SIZE_IN_FRAME)

# Initiating Aubio's pitch detection object.
pDetection = aubio.pitch(METHOD, BUFFER_SIZE,
    HOP_SIZE, SAMPLE_RATE)
# Set unit.
pDetection.set_unit("Hz")
# Frequency under -40 dB will considered
# as a silence.
pDetection.set_silence(-40)

client = speech.SpeechClient()



prevVol = 0.0


def record():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 2
    WAVE_OUTPUT_FILENAME = "output.raw"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    
    while(True):
        data = stream.read(CHUNK)
        frames.append(data)

        # Always listening to the microphone.
        data = mic.read(PERIOD_SIZE_IN_FRAME)
        # Convert into number that Aubio understand.
        samples = num.fromstring(data,
            dtype=aubio.float_type)
        # Compute the energy (volume)
        # of the current frame.
        volume = num.sum(samples**2)/len(samples)
        # Format the volume output so it only
        # displays at most six numbers behind 0.
        volume = "{:6f}".format(volume)
        print(volume)

        if(float(volume) > 0.005):
            break

        


            
        

    #for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        

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

def send_record():
    file_name = os.path.abspath('output.raw')
    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,sample_rate_hertz=44100,language_code='en-US')

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))
    



while(True):
    record()
    send_record()
    print("x")
