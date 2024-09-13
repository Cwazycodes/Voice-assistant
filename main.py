import os
from dotenv import load_dotenv
from openai_helper import OpenAIHelper
from gtts import gTTS
import speech_recognition as sr

load_dotenv()

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
            print("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            print("Sorry, there was an issue with the speech recognition service.")
            return ""

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save('output.mp3')
    os.system('afplay output.mp3') 

def main():
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        raise ValueError("OpenAI API key not found. Set the 'OPENAI_API_KEY' environment variable.")
    
    openai_helper = OpenAIHelper()
    
    print("Voice assistant is running. Say 'exit' to stop.")
    
    while True:
        command = listen_command()
        if command:
            if "exit" in command:  
                print("Exiting...")
                speak("Goodbye!")
                break
            
            response = openai_helper.ask_openai(command)
            if response:
                print(f"AI: {response}")
                speak(response)
            else:
                speak("Sorry, I couldn't process that.")

if __name__ == "__main__":
    main()