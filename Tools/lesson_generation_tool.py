# tools/lesson_generation_tool.py

from typing import Dict
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import json

class LessonGenerationTool:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.7,
            convert_system_message_to_human=True
        )

        self.prompt_template = PromptTemplate.from_template("""
You are an AI lesson co-teacher helping to generate structured lesson content for Indian classrooms.

Generate a JSON output with the following keys:
- topic_title
- introduction
- core_concepts (as a list of bullet points)
- explanation (detailed, regionalized)
- examples (optional, list form)
- summary
- suggested_agents (like "QuizAgent", "StoryTellerAgent")

Make it clear and culturally contextual based on the input dialect and difficulty level.

Topic: {topic}
Grade Level: {level}
Dialect: {dialect}

Respond ONLY in valid JSON format.
""")

    def run(self, inputs: Dict) -> str:
        topic = inputs.get("topic", "Photosynthesis")
        level = inputs.get("level", "Medium")
        dialect = inputs.get("dialect", "Telangana Telugu")

        prompt = self.prompt_template.format(topic=topic, level=level, dialect=dialect)
        result = self.llm.invoke(prompt)

        # Validate JSON
        try:
            parsed = json.loads(result.content)
            return parsed  # Return as Python dict (JSON serializable)
        except json.JSONDecodeError:
            return { 
                "error": "Lesson generation failed. Output was not valid JSON.",
                "raw_response": result.content
            }
