import os
from dotenv import load_dotenv
from openai_helper import OpenAIHelper
from gtts import gTTS
import speech_recognition as sr
import requests
import re
from datetime import datetime

load_dotenv()

WAKE_WORD = 'piper'

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            phrase = recognizer.recognize_google(audio).lower()
            print(f"You said: {phrase}")
            return phrase
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
    os.remove('output.mp3')

def get_weather(city):
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    data = response.json()
    if data["cod"] == 200:
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]
        return f"The temperature in {city} is {temperature}°C with {description}."
    else:
        return "Sorry, I couldn't fetch the weather data."

def extract_city_from_command(command):
    pattern = re.compile(r'weather in ([\w\s-]+)|in ([\w\s-]+)', re.IGNORECASE)
    match = pattern.search(command)
    if match:
        city = match.group(1) or match.group(2)
        return city.strip()
    return None

def get_current_time():
    now = datetime.now()
    return now.strftime("The current time is %H:%M.")

def main():
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        raise ValueError("OpenAI API key not found. Set the 'OPENAI_API_KEY' environment variable.")
    
    openai_helper = OpenAIHelper()

    print("Voice assistant is running. Say 'exit' at any time to stop. Say 'Piper' to wake assistant.")
    
    while True:
        phrase = listen_for_command()
        
        if not phrase:
            continue

        if "exit" in phrase:
            print("Exiting...")
            speak("Goodbye! Feel free to return if you have more questions or need assistance. Have a great day!")
            break

        if WAKE_WORD in phrase:
            speak('Yes, how can I help you?')
            
            command = listen_for_command()
            if command:
                if "exit" in command.lower():
                    print("Exiting...")
                    speak("Goodbye! Feel free to return if you have more questions or need assistance. Have a great day!")
                    break

                if "weather" in command.lower():
                    city = extract_city_from_command(command)
                    if city:
                        weather_info = get_weather(city)
                        print(f"Weather info: {weather_info}")
                        speak(weather_info)
                    else:
                        speak("Sorry, I couldn't detect the city. Please specify the city.")
                    continue

                if "time" in command.lower():
                    time_info = get_current_time()
                    print (f"Time info: {time_info}")
                    speak(time_info)
                    continue 
                
                response = openai_helper.ask_openai(command)
                if response:
                    print(f"AI: {response}")
                    speak(response)
                else:
                    speak("Sorry, I couldn't process that.")

if __name__ == "__main__":
    main()