# Voice Assistant - Piper

## Overview

Piper is a voice-controlled assistant designed to respond to spoken commands. It uses OpenAI's GPT for handling general queries, provides weather updates, and tells the current time. This project consists of a Python backend and a JavaScript frontend, along with a simple HTML interface.

## Features

- **Voice Activation**: Start the assistant with the wake word "Piper."
- **Weather Information**: Get the current weather by specifying a city.
- **Time Inquiry**: Ask for the current time.
- **OpenAI Integration**: Ask general questions and receive responses from GPT-3.
- **Speech Synthesis**: Responses are spoken out loud using text-to-speech.

## Setup

### Prerequisites

Ensure you have Python 3.x and Node.js installed.

### Python Backend

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set Up Environment Variables**

   Create a `.env` file in the root directory with the following content:
   ```makefile
   OPENAI_API_KEY=<your-openai-api-key>
   OPENWEATHERMAP_API_KEY=<your-openweathermap-api-key>
   ```

6. **Run the Flask Application**
   ```bash
   python app.py
   ```

   The Flask server will start on `http://localhost:9000`.

### Frontend Setup

1. **Navigate to the Static Directory**

   Ensure your static files (`app.js`, `styles.css`) are located in a `static` directory.

2. **Open the HTML File**

   Open `index.html` in a web browser to access the voice assistant interface.

## Usage

1. **Activate Piper**

   Say "Piper" to activate the assistant.

2. **Issue Commands**

   After activation, you can issue commands such as:
   - "What's the weather like in [city]?"
   - "What time is it?"
   - "Who is the president of the United States?"

3. **Exit**

   To stop the assistant, say "exit."

## Testing

To ensure everything works correctly, run the provided tests:

```bash
pytest
```

These tests cover core functionalities like speech recognition, weather fetching, and OpenAI integration.

## Troubleshooting

- **Speech Recognition Issues**: Ensure your microphone is functioning and browser permissions are set correctly.
- **API Key Errors**: Verify your `.env` file has the correct API keys and that they are active.
- **Server Issues**: Make sure Flask is running and that you're accessing the correct URL.


## Author

Muhammad Hussain - [GitHub](https://github.com/Cwazycodes)
