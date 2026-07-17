from google import genai
import os
import json
from backend.config import settings
from backend.prompts.cleaning_prompt import build_cleaning_prompt


client = genai.Client(api_key=settings.GEMINI_API_KEY)

class LLMService:
    def generate_cleaning_plan(self,report:dict):
        prompt = build_cleaning_prompt(report)

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
        )


        return json.loads(response.text)
