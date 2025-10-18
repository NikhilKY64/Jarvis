import tkinter as tk
from tkinter import scrolledtext
import webbrowser
import pyautogui
import pywhatkit as pwk
import requests
from bs4 import BeautifulSoup

def speak(text):
    chatbox.insert(tk.END, "Jarvis: " + text + "\n")
    chatbox.yview(tk.END)

def process_command(command):
    command = command.lower()

    if "hello" in command:
        speak("Welcome to Jarvis, how can I help you?")
        
    elif "what is your name" in command or "what's your name" in command:
        speak("My name is Jarvis.")
        
    elif "open central board" in command:
        webbrowser.open("https://www.cbse.gov.in/cbsenew/cbse.html")
        speak("Opening CBSE official site.")      

    elif "open academic" in command:
        webbrowser.open("https://cbseacademic.nic.in/")
        speak("Opening CBSE Academic site.")
        
    elif "open vigyan" in command:
        webbrowser.open("https://www.youtube.com/@VigyanRecharge/videos")
        speak("Opening Vigyan Recharge.")  
        
    elif "open amazon" in command:
        webbrowser.open("https://www.amazon.in/s?k=")
        speak("Opening Amazon.")  
        
    elif "search amazon" in command:
        query = command.replace("search amazon", "").strip()
        webbrowser.open("https://www.amazon.in/s?k=" + query)
        speak(f"Searching Amazon for {query}.")  
        
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")  
        
    elif "search youtube" in command:
        query = command.replace("search youtube", "").strip()
        webbrowser.open("https://www.youtube.com/results?search_query=" + query)
        speak(f"Searching YouTube for {query}.")
        
    elif "open" in command:
        app = command.replace("open", "").strip()
        pyautogui.press('super')
        pyautogui.typewrite(app)
        pyautogui.sleep(2)
        pyautogui.press('enter')
        speak(f"Opening {app}.")  
        
    elif "search" in command:
        query = command.replace("search", "").strip()
        webbrowser.open("https://www.google.com/search?q=" + query)
        speak(f"Searching Google for {query}.")      
    
    elif "send whatsapp" in command:
        speak("Sending WhatsApp message...")
        pwk.sendwhatmsg("+918858540320", "Hi", 11, 12)
    
    elif "temperature" in command or "weather" in command:
        location = "prayagraj"
        search = f"temperature in {location}"
        url = f"https://www.google.com/search?q={search}"
        r = requests.get(url)
        data = BeautifulSoup(r.text, "html.parser")
        temp = data.find("div", class_="BNeawe").text
        speak(f"Current temperature in {location} is {temp}.")
    
    elif "are you listening" in command:
        speak("Yes, I am listening.")

    elif "go to sleep" in command or "exit" in command or "final sleep" in command:
        speak("Going to final sleep. Goodbye.")
        root.after(2000, root.destroy)
    
    else:
        speak("Sorry, I didn't understand that command.")

def on_enter(event=None):
    user_input = entry.get().strip()
    if user_input:
        chatbox.insert(tk.END, "You: " + user_input + "\n")
        chatbox.yview(tk.END)
        entry.delete(0, tk.END)
        process_command(user_input)

# GUI Setup
root = tk.Tk()
root.title("Jarvis - Chat Mode")
root.geometry("600x500")
root.config(bg="#1e1e1e")

chatbox = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12), bg="#2d2d2d", fg="white")
chatbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry = tk.Entry(root, font=("Arial", 12), bg="#333", fg="white")
entry.pack(padx=10, pady=(0, 10), fill=tk.X)
entry.bind("<Return>", on_enter)

entry.focus()
speak("Jarvis is ready. Type 'hello' or 'wake up' to begin.")

root.mainloop()
