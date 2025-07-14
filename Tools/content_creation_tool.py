from typing import Dict
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import json

class ContentCreationTool:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.5)
        self.prompt_template = PromptTemplate.from_template("""
You are a content fusion assistant for VidyaVāhinī.

Given teacher notes and an AI-generated lesson, blend both to create a coherent, engaging lesson.

Respond only in JSON with keys:
- title
- combined_lesson
- teacher_notes_used

Teacher Notes: {notes}
AI Lesson Snippet: {lesson}
Dialect: {dialect}
Grade Level: {level}
""")

    def run(self, inputs: Dict) -> Dict:
        notes = inputs.get("notes", "")
        lesson = inputs.get("lesson", "")
        level = inputs.get("level", "6")
        dialect = inputs.get("dialect", "Telangana Telugu")

        prompt = self.prompt_template.format(
            notes=notes, lesson=lesson, level=level, dialect=dialect
        )
        response = self.llm.invoke(prompt)

        try:
            return json.loads(response.content)
        except Exception:
            return {"error": "Content creation failed", "raw_output": response.content}