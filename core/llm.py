from openai import OpenAI
import os

class GroqLLM:
    def __init__(self, model="mixtral-8x7b-32768", api_key=None, base_url="https://api.groq.com/openai/v1"):
        self.client = OpenAI(api_key=api_key or os.getenv("GROQ_API_KEY"), base_url=base_url)
        self.model = model

    def call(self, prompt, system_prompt=None):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2
        )
        return completion.choices[0].message.content
