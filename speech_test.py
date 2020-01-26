import speech_recognition as sr
#quiet the endless 'insecurerequest' warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

while (True == True):
# obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        #print("Please wait. Calibrating microphone...")
        # listen for 1 second and create the ambient noise energy level
        r.adjust_for_ambient_noise(source, duration=1)
        print("Say something!")
        audio = r.listen(source,phrase_time_limit=5)
    try:
        response = r.recognize_google(audio)
        print("I think you said '" + response + "'")
        tts = gTTS(text="I think you said "+str(response), lang='en')
        tts.save("response.mp3")
        mixer.music.load('response.mp3')
        mixer.music.play()
    except:
        print("Sphinx could not understand audio")
    