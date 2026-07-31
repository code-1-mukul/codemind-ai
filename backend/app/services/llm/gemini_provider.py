import os
from app.core.config import settings
from google import genai

class GeminiProvider:

    def __init__(self):

        self.api_key = settings.GEMINI_API_KEY
        
        if not self.api_key:
            raise ValueError("Gemini API key not found. Please check your .env file")

        self.client = genai.Client(api_key=self.api_key)

    def generate_response(self, prompt:str) -> str:

        response = self.client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        return response.text

