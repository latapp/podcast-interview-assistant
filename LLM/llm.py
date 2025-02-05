from openai import OpenAI
from rich import print
from pydantic import BaseModel
from config import BASE_PROMPT, LLM_MODEL, MODEL_API_KEY, MODEL_BASE_URL

class ModelResponse(BaseModel):
    questions: list[str]


class LLM:
    def __init__(self):
        self.model = LLM_MODEL
        self.openai = OpenAI(
            api_key=MODEL_API_KEY,
            base_url=MODEL_BASE_URL
        )
    
    def generate(self, text: str | list[str]) -> str:
        if type(text) == str:
            text = [text]
        elif type(text) != list:
            raise ValueError("El parametro text debe ser un string o una lista de strings")

        completion =  self.openai.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role":"system","content": BASE_PROMPT},
                {"role":"user","content":" ".join(text)}
            ],
            response_format=ModelResponse
        )

        return completion.choices[0].message.content
