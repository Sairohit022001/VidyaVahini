from typing import Dict
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import json

class QuizGenerationTool:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.5,
            google_api_key=os.getenv("GEMINI_API_KEY")
        )

        self.prompt_template = PromptTemplate.from_template("""
You are a quiz creation assistant for Indian school teachers.
Based on the lesson content and story context, generate a quiz in JSON format.

Output keys:
- topic
- grade_level
- dialect
- questions (5)
- options (list per question)
- correct_answers
- explanation (optional)
- mode: "MCQ", "FillBlanks", or "TrueFalse"
- retry_logic: true/false

Topic: {topic}
Level: {level}
Dialect: {dialect}
StoryContext: {story_context}

Ensure cultural and dialect localization, and ensure no repetition.
""")

    def run(self, inputs: Dict) -> Dict:
        topic = inputs.get("topic", "Photosynthesis")
        level = inputs.get("level", "Medium")
        dialect = inputs.get("dialect", "Telangana Telugu")
        story_context = inputs.get("story_context", "")

        prompt = self.prompt_template.format(
            topic=topic,
            level=level,
            dialect=dialect,
            story_context=story_context
        )

        result = self.llm.invoke(prompt)
        try:
            return json.loads(result.content)
        except json.JSONDecodeError:
            return {"error": "Quiz generation failed", "raw_output": result.content}
