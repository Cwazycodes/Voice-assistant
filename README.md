Here’s a README file for your project, explaining its purpose, how to set it up, and how to use it:

Voice Assistant - Piper

Overview

Piper is a voice-controlled assistant designed to respond to spoken commands. It uses OpenAI's GPT for handling general queries, provides weather updates, and tells the current time. This project consists of a Python backend and a JavaScript frontend, along with a simple HTML interface.

Features

Voice Activation: Start the assistant with the wake word "Piper."
Weather Information: Get the current weather by specifying a city.
Time Inquiry: Ask for the current time.
OpenAI Integration: Ask general questions and receive responses from GPT-3.
Speech Synthesis: Responses are spoken out loud using text-to-speech.
Setup

Prerequisites
Ensure you have Python 3.x and Node.js installed.

Python Backend
Clone the Repository
bash
Copy code
git clone <repository-url>
cd <repository-directory>
Create a Virtual Environment
bash
Copy code
python -m venv venv
Activate the Virtual Environment
On Windows:
bash
Copy code
venv\Scripts\activate
On macOS/Linux:
bash
Copy code
source venv/bin/activate
Install Dependencies
bash
Copy code
pip install -r requirements.txt
Set Up Environment Variables
Create a .env file in the root directory with the following content:

makefile
Copy code
OPENAI_API_KEY=<your-openai-api-key>
OPENWEATHERMAP_API_KEY=<your-openweathermap-api-key>
Run the Flask Application
bash
Copy code
python app.py
The Flask server will start on http://localhost:9000.
Frontend Setup
Navigate to the Static Directory
Your static files (CSS and JavaScript) should be in a static directory. Ensure that app.js and styles.css are located in this directory.
Open the HTML File
Open index.html in a web browser to access the voice assistant interface.
Usage

Activate Piper
Say "Piper" to activate the assistant.
Issue Commands
After activation, you can issue commands like:

"What's the weather like in [city]?"
"What time is it?"
"Who is the president of the United States?"
Exit
To stop the assistant, say "exit."
Testing

To ensure everything is working correctly, you can run the provided tests using:

bash
Copy code
pytest
These tests cover the core functionalities of the application, including speech recognition, weather fetching, and integration with OpenAI.

Troubleshooting

Speech Recognition Issues: Ensure your microphone is working and that browser permissions are set correctly.
API Key Errors: Check that your .env file has the correct API keys and that the keys are active.
Server Issues: Ensure that Flask is running and that you are accessing the correct URL.
License


Author

Muhammad Hussain - https://github.com/Cwazycodes
