import openai
import os

class OpenAIHelper:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.conversation_history = []
    
    def ask_openai(self, prompt):
        if not prompt or not isinstance(prompt, str):
            print("Invalid prompt provided.")
            return None
        self.conversation_history.append({"role": "user", "content": prompt})
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.conversation_history,
            )
            reply = response['choices'][0]['message']['content']
            self.conversation_history.append({"role": "assistant", "content": reply})
            return reply
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None