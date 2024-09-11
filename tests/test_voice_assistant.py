from openai_helper import OpenAIHelper
from unittest.mock import patch

def test_openai_response():
    openai_helper = OpenAIHelper("fake-api-key")
    
    with patch('openai.resources.chat.Completions.create') as mock_openai:
        mock_openai.return_value = {'choices': [{'message': {'content': "I am an AI assistant"}}]}
        
        response = openai_helper.ask_openai("Hello, who are you?")
        assert "I am an AI assistant" in response