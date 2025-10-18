import pyttsx3
import speech_recognition as sr
#import mtranslate
import webbrowser
import pyautogui
import pywhatkit as pwk
import requests
from bs4 import BeautifulSoup
import openai

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 175)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
     
def command():
    content = ""
    while not content.strip():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)

        try:
            content = r.recognize_google(audio, language='en-in')
            #rint("You Said  " + content)
            #content = mtranslate.translate(content,to_language='en-in')
            print("You Said  " + content)
        except Exception as e:
            print("Please try again ... ")

    return content
speak("I'm sleeping.")

def main_process():
    while True:
        request = command().lower()
        if "wake up" in request:
            from JarvisFunction import Jarvis_st_Function
            Jarvis_st_Function()

            while True:
                request = command().lower()
                if "go to sleep" in request or "so ja munna so ja" in request:
                    request = request.replace("jarvis ", "")
                    speak("Ok , You can me call anytime")
                    break

                elif "hello" in request:
                    request = request.replace("jarvis ", "")
                    speak("welcome to jarvis, How can I help you?")
                elif "what is your name" in request:
                    speak("My name is Jarvis.")
                elif "what's your name" in request:
                    speak("My name is Jarvis.")

                elif "open central board" in request:
                    request = request.replace("jarvis ", "")
                    webbrowser.open("https://www.cbse.gov.in/cbsenew/cbse.html")
                    speak("okay")      
                    
                elif "open academic" in request:
                    request = request.replace("jarvis ", "")
                    webbrowser.open("https://cbseacademic.nic.in/")
                    speak("okay")
                        
                elif "open vigyan" in request:
                    request = request.replace("jarvis ", "")
                    webbrowser.open("https://www.youtube.com/@VigyanRecharge/videos")
                    speak("okay")  
                    
                elif "open amazon" in request:
                    request = request.replace("jarvis ", "")
                    webbrowser.open("https://www.amazon.in/s?k=")
                    speak("okay")  
                    
                elif "search amazon" in request:
                    request = request.replace("jarvis ", "")
                    request = request.replace("search amazon ", "")
                    webbrowser.open("https://www.amazon.in/s?k="+request)
                    speak("okay")  
                    
                elif "open with chat" in request:
                    request = request.replace("jarvis ", "")
                    webbrowser.open("https://chatgpt.com/")
                    speak("okay")  
                    
                elif "open youtube" in request:
                    request = request.replace("jarvis ", "")
                    webbrowser.open("https://www.youtube.com")
                    speak("okay")  
                    
                elif "search youtube" in request:
                    request = request.replace("jarvis ", "")
                    request = request.replace("search youtube ", "")
                    webbrowser.open("https://www.youtube.com/results?search_query="+request)
                    speak("okay")
                    
                elif "open" in request:
                    request = request.replace("jarvis ", "")
                    request = request.replace("open ", "")
                    pyautogui.press('super')
                    pyautogui.typewrite(request)
                    pyautogui.sleep(2)
                    pyautogui.press('enter')
                    speak("okay")  
                    
                elif "search " in request:
                    request = request.replace("jarvis ", "")
                    request = request.replace("search ", "")
                    webbrowser.open("https://www.google.com/search?q="+request)
                    speak("okay")      
                
                           
                elif "send whatsapp" in request:
                    request = request.replace("jarvis ", "")
                    message = "Hi"
                    pwk.sendwhatmsg("+918858540320", message, 11, 12, 28)
                    break
                    
                elif "whatsapp" in request:
                    request = request.replace("jarvis", "")
                    pyautogui.typewriter(request)
                    pyautogui.sleep(2.5)
                    pyautogui.press('enter')
                
                elif "temperature now" in request:
                    request = request.replace("jarvis ", "")
                    search = "temperature in prayagraj"
                    url = f"https://www.google.com/search?q=temperature+in+{search}"
                    r  = requests.get(url)
                    data = BeautifulSoup(r.text,"html.parser")
                    temp = data.find("div", class_ = "BNeawe").text
                    speak(f"current{search} is {temp}")
                elif "weather" in request:
                    search = "temperature in prayagraj"
                    url = f"https://www.google.com/search?q=temperature+in+{search}"
                    r  = requests.get(url)
                    data = BeautifulSoup(r.text,"html.parser")
                    temp = data.find("div", class_ = "BNeawe").text
                    speak(f"current{search} is {temp}")
                    
                elif "are you listening" in request:
                    request = request.replace("jarvis ", "")
                    speak("yes, I am listening.")
                
                elif "go to final sleep" in request   or "final sleep" in request:
                    from JarvisFunction import JarvisedFunction
                    JarvisedFunction()
                    
        elif "are you listening" in request:
                    request = request.replace("jarvis ", "")
                    speak("yes, I am listening.")
                            
        elif "go to final sleep" in request or "final sleep" in request:
            from JarvisFunction import Jarvis_ed_Function
            Jarvis_ed_Function()
  
if __name__ == "__main__":
    main_process()