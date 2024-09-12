from openai_helper import OpenAIHelper
from unittest.mock import patch
import pyttsx3
import speech_recognition as sr
from main import speak, listen_command

def test_openai_response():
    openai_helper = OpenAIHelper("fake-api-key")
    
    with patch('openai.resources.chat.Completions.create') as mock_openai:
        mock_openai.return_value = {'choices': [{'message': {'content': "I am an AI assistant"}}]}
        
        response = openai_helper.ask_openai("Hello, who are you?")
        assert "I am an AI assistant" in response

def test_speak():
    with patch('pyttsx3.init') as mock_init:
        mock_engine = mock_init.return_value
        
        mock_engine.say = patch('pyttsx3.Engine.say').start()
        mock_engine.runAndWait = patch('pyttsx3.Engine.runAndWait').start()
        
        speak("Hello World")
        
        mock_engine.say.assert_called_once_with("Hello World")
        mock_engine.runAndWait.assert_called_once()

        patch.stopall()
        
@patch('speech_recognition.Recognizer.recognize_google', return_value="Test command")
def test_listen_command(mock_recognize):
    command = listen_command()
    assert command == "Test command"