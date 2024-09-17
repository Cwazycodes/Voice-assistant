from openai_helper import OpenAIHelper
from unittest.mock import patch, MagicMock
from gtts import gTTS
import speech_recognition as sr
from main import speak, listen_for_command, get_weather, main
import os

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
    with patch('main.gTTS') as mock_gtts, \
         patch('os.system') as mock_system, \
         patch('os.remove') as mock_remove:  
        
        mock_gtts_instance = mock_gtts.return_value
        mock_gtts_instance.save = MagicMock()

        speak("Hello World")
        
        mock_gtts_instance.save.assert_called_once_with('output.mp3')
        
        mock_system.assert_called_once_with('afplay output.mp3')
        
        mock_remove.assert_called_once_with('output.mp3')


@patch('speech_recognition.Recognizer.recognize_google', return_value="Test command")
def test_listen_for_command(mock_recognize):
    command = listen_for_command()
    assert command == "test command"

@patch('requests.get')
def test_get_weather(mock_get):
    mock_get.return_value.json.return_value = {
        "cod": 200,
        "main": {"temp": 20},
        "weather": [{"description": "clear sky"}]
    }
    result = get_weather("London")
    assert "20°C with clear sky" in result

@patch('openai.ChatCompletion.create')
def test_context_awareness(mock_openai):
    openai_helper = OpenAIHelper()

    mock_openai.side_effect = [
        {'choices': [{'message': {'content': 'The president of the United States is Joe Biden.'}}]},
        {'choices': [{'message': {'content': 'He is 81 years old.'}}]}
    ]
    
    response1 = openai_helper.ask_openai("Who is the president of the United States?")
    assert response1 == "The president of the United States is Joe Biden."

    response2 = openai_helper.ask_openai("How old is he?")
    assert response2 == "He is 81 years old."

    assert len(openai_helper.conversation_history) == 4
    assert openai_helper.conversation_history[0] == {"role": "user", "content": "Who is the president of the United States?"}
    assert openai_helper.conversation_history[1] == {"role": "assistant", "content": "The president of the United States is Joe Biden."}
    assert openai_helper.conversation_history[2] == {"role": "user", "content": "How old is he?"}
    assert openai_helper.conversation_history[3] == {"role": "assistant", "content": "He is 81 years old."}

@patch('speech_recognition.Recognizer.recognize_google')
def test_exit_command(mock_recognize):
    mock_recognize.side_effect = ["exit"]
    
    assert listen_for_command() == "exit"

@patch('speech_recognition.Recognizer.recognize_google')
def test_wake_word(mock_recognize):
    mock_recognize.side_effect = ["piper"]
    
    assert listen_for_command() == "piper"

@patch('main.listen_for_command')
@patch('main.speak')
@patch('openai.ChatCompletion.create')
def test_main_exit(mock_openai, mock_speak, mock_listen_for_command):
    mock_listen_for_command.side_effect = ["piper", "exit"] 

    main()

    mock_speak.assert_called_with("Goodbye! Feel free to return if you have more questions or need assistance. Have a great day!")

@patch('main.listen_for_command')
@patch('main.speak')
@patch('main.requests.get')
def test_main_wake_word(mock_requests_get, mock_speak, mock_listen_for_command):
    mock_requests_get.return_value.json.return_value = {
        "cod": 200,
        "main": {"temp": 15},
        "weather": [{"description": "clear skies"}]
    }

    mock_listen_for_command.side_effect = ["piper", "What's the weather in London?", "exit"]

    main()

    mock_speak.assert_any_call('The temperature in London is 15°C with clear skies.')