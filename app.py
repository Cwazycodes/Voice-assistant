from flask import Flask, jsonify, request, render_template
import os
from dotenv import load_dotenv
from openai_helper import OpenAIHelper
from gtts import gTTS
import speech_recognition as sr
import requests
from datetime import datetime
import re

load_dotenv()

app = Flask(__name__)

WAKE_WORD = 'piper'

openai_helper = OpenAIHelper()

recognizer = sr.Recognizer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/listen', methods=['GET'])
def listen_for_command():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
            phrase = recognizer.recognize_google(audio).lower()
            print(f"You said: {phrase}")
            return jsonify({"command": phrase})
    except sr.UnknownValueError:
        return jsonify({"error": "Sorry, I did not understand that."}), 400
    except sr.RequestError:
        return jsonify({"error": "Speech recognition service error."}), 500

@app.route('/speak', methods=['POST'])
def speak():
    text = request.json.get('text')
    if text:
        tts = gTTS(text=text, lang='en')
        tts.save('output.mp3')
        os.system('afplay output.mp3') 
        os.remove('output.mp3')
        return jsonify({"message": "Spoken: " + text})
    else:
        return jsonify({"error": "No text provided."}), 400

@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.json.get('city')
    if city:
        api_key = os.getenv('OPENWEATHERMAP_API_KEY')
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(base_url)
        data = response.json()
        if data["cod"] == 200:
            temperature = data["main"]["temp"]
            description = data["weather"][0]["description"]
            return jsonify({"weather": f"The temperature in {city} is {temperature}°C with {description}."})
        else:
            return jsonify({"error": "Could not fetch the weather data."}), 400
    else:
        return jsonify({"error": "City not provided."}), 400

@app.route('/time', methods=['GET'])
def get_current_time():
    now = datetime.now()
    time_info = now.strftime("The current time is %H:%M.")
    return jsonify({"time": time_info})

@app.route('/ask', methods=['POST'])
def ask_openai():
    command = request.json.get('command')
    if command:
        response = openai_helper.ask_openai(command)
        if response:
            return jsonify({"response": response})
        else:
            return jsonify({"error": "Unable to process command."}), 500
    else:
        return jsonify({"error": "No command provided."}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)