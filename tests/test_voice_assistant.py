from openai_helper import OpenAIHelper
from unittest.mock import patch, MagicMock
from gtts import gTTS
import speech_recognition as sr
from main import speak, listen_command, get_weather

def test_openai_response():
    openai_helper = OpenAIHelper()

    with patch('openai.ChatCompletion.create') as mock_openai:
        mock_openai.return_value = {
            'choices': [
                {'message': {'content': 'Test response from OpenAI'}}
            ]
        }

        response = openai_helper.ask_openai("Test prompt")
        assert response == "Test response from OpenAI"

def test_speak():
    with patch('main.gTTS') as mock_gtts:
        mock_gtts_instance = mock_gtts.return_value
        mock_gtts_instance.save = MagicMock()

        speak("Hello World")


        mock_gtts_instance.save.assert_called_once_with('output.mp3')
        

        mock_gtts.assert_called_once_with(text="Hello World", lang='en')

@patch('speech_recognition.Recognizer.recognize_google', return_value="Test command")
def test_listen_command(mock_recognize):
    command = listen_command()
    assert command == "Test command"

@patch('requests.get')
def test_get_weather(mock_get):
    mock_get.return_value.json.return_value = {
        "cod": 200,
        "main": {"temp": 20},
        "weather": [{"description": "clear sky"}]
    }
    result = get_weather("London")
    assert "20°C with clear sky" in result