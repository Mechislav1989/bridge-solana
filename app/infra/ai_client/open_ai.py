from dataclasses import dataclass
from openai import OpenAI

from domain.values.contract import Code


@dataclass
class OpenAIAdapter:
    api_key: str

    def generate_code(self, prompt: str) -> Code:
        client = OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': prompt}]
        )
        return Code.from_ai_response(response.choices[0].message.content)