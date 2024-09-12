import speech_recognition as sr 
from openai_helper import OpenAIHelper
import pyttsx3

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
        except sr.RequestError:
            print("API unavailable.")

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()