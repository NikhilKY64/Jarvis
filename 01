import webbrowser
import pyautogui
import pywhatkit as pwk
import requests
from bs4 import BeautifulSoup

# Speak function replaced with print
def speak(text):
    print("Jarvis:", text)

# Command function replaced with input
def command():
    return input("You: ").lower()

def main_process():
    speak("I am in chat mode. Type 'wake up' to start.")
    
    while True:
        request = command()
        
        if "wake up" in request:
            speak("Jarvis activated. How can I help you?")
            
            while True:
                request = command()
                
                if "go to sleep" in request:
                    speak("Okay, you can call me anytime.")
                    break

                elif "hello" in request:
                    speak("Welcome to Jarvis, how can I help you?")

                elif "what is your name" in request or "what's your name" in request:
                    speak("My name is Jarvis.")

                elif "open central board" in request:
                    webbrowser.open("https://www.cbse.gov.in/cbsenew/cbse.html")
                    speak("Opening CBSE official site.")      

                elif "open academic" in request:
                    webbrowser.open("https://cbseacademic.nic.in/")
                    speak("Opening CBSE Academic site.")
                    
                elif "open vigyan" in request:
                    webbrowser.open("https://www.youtube.com/@VigyanRecharge/videos")
                    speak("Opening Vigyan Recharge.")  
                    
                elif "open amazon" in request:
                    webbrowser.open("https://www.amazon.in/s?k=")
                    speak("Opening Amazon.")  
                    
                elif "search amazon" in request:
                    query = request.replace("search amazon", "").strip()
                    webbrowser.open("https://www.amazon.in/s?k=" + query)
                    speak(f"Searching Amazon for {query}.")  
                    
                elif "open with chat" in request:
                    webbrowser.open("https://chatgpt.com/")
                    speak("Opening ChatGPT.")  
                    
                elif "open youtube" in request:
                    webbrowser.open("https://www.youtube.com")
                    speak("Opening YouTube.")  
                    
                elif "search youtube" in request:
                    query = request.replace("search youtube", "").strip()
                    webbrowser.open("https://www.youtube.com/results?search_query=" + query)
                    speak(f"Searching YouTube for {query}.")
                    
                elif "open" in request:
                    app = request.replace("open", "").strip()
                    pyautogui.press('super')
                    pyautogui.typewrite(app)
                    pyautogui.sleep(2)
                    pyautogui.press('enter')
                    speak(f"Opening {app}.")  
                    
                elif "search" in request:
                    query = request.replace("search", "").strip()
                    webbrowser.open("https://www.google.com/search?q=" + query)
                    speak(f"Searching Google for {query}.")      
                
                elif "send whatsapp" in request:
                    message = input("Enter your message: ")
                    time_hr = int(input("Hour (24-hour format): "))
                    time_min = int(input("Minute: "))
                    pwk.sendwhatmsg("+918858540320", message, time_hr, time_min)
                    speak("Sending WhatsApp message.")
                    break
                    
                elif "temperature now" in request or "weather" in request:
                    location = input("Enter city name: ") or "prayagraj"
                    search = f"temperature in {location}"
                    url = f"https://www.google.com/search?q={search}"
                    r = requests.get(url)
                    data = BeautifulSoup(r.text, "html.parser")
                    temp = data.find("div", class_="BNeawe").text
                    speak(f"Current temperature in {location} is {temp}.")
                
                elif "are you listening" in request:
                    speak("Yes, I am listening.")

                elif "go to final sleep" in request or "final sleep" in request:
                    speak("Going to final sleep. Goodbye.")
                    exit()

        elif "go to final sleep" in request:
            speak("Going to final sleep. Goodbye.")
            exit()

if __name__ == "__main__":
    main_process()
