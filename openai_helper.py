from openai import OpenAI



class OpenAIHelper:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def ask_openai(self, prompt):
        response = self.client.chat.completions.create(model='gpt-3.5-turbo', messages=[{"role":"user", "content": prompt}])
        return response['choices'][0]['message']['content'].strip()