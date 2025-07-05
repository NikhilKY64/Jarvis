import pyttsx3
import datetime

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate",200)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def Jarvis_st_Function():
    hour  = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("Good Morning")
    if hour>=12 and hour<=18:
        speak("Good Afternoon")
    if hour>=18 and hour<=24:
        speak("Good Evening")

    speak("Please tell me, How can I help you ?")

def Jarvis_ed_Function():
    hour  = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("okay, bye!")
    if hour>=12 and hour<=22:
        speak("okay, bye!")
    if hour>=22 and hour<=24:
        speak("It's very late, you should sleep, Good Night")
    exit()