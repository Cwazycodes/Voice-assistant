import openai
import os

class OpenAIHelper:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
    
    def ask_openai(self, prompt):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None