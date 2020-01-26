import argparse

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types  
import speech_recognition as sr 

import sounddevice as sd
import numpy as np




def analyze(content):
    """Run a sentiment analysis request on text within a passed filename."""
    client = language.LanguageServiceClient()

    document = types.Document(
        content=content,
        type=enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(document=document)

    # Print the results
    print(annotations)
  
#enter the name of usb microphone that you found 
#using lsusb 
#the following name is only used as an example 
mic_name = "Microphone (HD Webcam C270)"
#Sample rate is how often values are recorded 
sample_rate = 48000
#Chunk is like a buffer. It stores 2048 samples (bytes of data) 
#here.  
#it is advisable to use powers of 2 such as 1024 or 2048 
chunk_size = 2048
#Initialize the recognizer 
r = sr.Recognizer() 
  
#generate a list of all audio cards/microphones 
mic_list = sr.Microphone.list_microphone_names() 

r.energy_threshold = 100
  
#the following loop aims to set the device ID of the mic that 
#we specifically want to use to avoid ambiguity. 
 
#use the microphone as source for input. Here, we also specify  
#which device ID to specifically look for incase the microphone  
#is not working, an error will pop up saying "device_id undefined" 
while(True):
    with sr.Microphone() as source: 
        #wait for a second to let the recognizer adjust the  
        #energy threshold based on the surrounding noise level 
        
        
        #listens for the user's input 
        audio = r.listen(source, phrase_time_limit=4)
        
        
            
        try: 
            text = r.recognize_google(audio) 
            print(text)
            analyze(text)
        
        #error occurs when google could not understand what was said 
        
        except sr.UnknownValueError: 
            print("Google Speech Recognition could not understand audio") 
        
        except sr.RequestError as e: 
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
    