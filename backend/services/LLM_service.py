from google import genai
import os
import json
from backend.config import settings
from backend.prompts.cleaning_prompt import build_cleaning_prompt
from backend.prompts.business_understanding_prompt import business_understanding
from backend.prompts.sql_prompt import build_sql_prompt
from backend.prompts.sql_summary_prompt import build_sql_summary_prompt
from backend.prompts.visualization_prompt import build_visualization_prompt


client = genai.Client(api_key=settings.GEMINI_API_KEY)

class LLMService:

    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = "gemini-3.5-flash"


    def generate_cleaning_plan(self,report:dict):
        prompt = build_cleaning_prompt(report)

        response = client.models.generate_content(
            model=self.model,
            contents=prompt,
        )


        return json.loads(response.text)

    def generate_business_summary(self,business_report:dict):
        prompt = business_understanding(business_report)

        response = client.models.generate_content(
            model=self.model,
            contents=prompt

        )

        return json.loads(response.text)
    
    def generate_sql(self,schema:dict, question:str) -> str:
        prompt = build_sql_prompt(schema=schema,question=question)

        response = self.client.models.generate_content(
        model=self.model,
        contents=prompt
    )

        sql = response.text.strip()

        sql = sql.replace("```sql", "")
        sql = sql.replace("```", "")
        sql = sql.strip()

        return sql
    
    def summarize_sql_result(self, question: str, results: list) -> str:

        prompt = build_sql_summary_prompt(
            question,
            results
        )

        response = self.client.models.generate_content(
        model=self.model,
        contents=prompt
    )
        
        return response.text
    
    def generate_visualization_plan(self, question: str, dataframe: object) -> dict:
        """
        Generate a visualization plan from the SQL result.

        Returns:
        {
            "chart_type": "bar",
            "x_column": "category",
            "y_column": "revenue",
            "title": "Revenue by Category"
        }
        """

        prompt = build_visualization_prompt(
            question=question,
            dataframe=dataframe
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        text = response.text.strip()

        # Remove markdown if Gemini returns it
        text = text.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(text)

        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON returned by Gemini:\n{text}"
            ) from e



            
            

