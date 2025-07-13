from typing import Dict
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI  # Gemini
import json

class StoryGenerationTool:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.75)

        self.prompt_template = PromptTemplate.from_template("""
You are a culturally aware story generation agent for Indian classrooms.

Given the topic, dialect, grade, and storytelling mode, generate a localized, original story for classroom teaching.

Use the following storytelling modes:
- 'modern': relatable school-life stories
- 'moral': everyday tales with a moral lesson
- 'mythological': inspired by Sanātana Dharma, Purāṇas, or epics
- 'folk': local village/tribal folk tales

Output Format: STRICTLY valid JSON with these keys:
- title
- story_body
- moral
- suggested_visuals (list of 3–5 short scene-level prompts)
- dialect
- story_mode

Use age-appropriate tone:
- Grades 1–5 → simple, fun storytelling
- Grades 6–10 → balance emotion with depth
- Grade 11+ → abstract, metaphorical storytelling

Use the dialect for tone and cultural flavor, not full translation.

INPUTS:
Topic: {topic}
Grade Level: {grade}
Dialect: {dialect}
Story Mode: {story_mode}

Respond only with valid JSON, no markdown, comments, or explanation.
""")

    def run(self, inputs: Dict) -> Dict:
        topic = inputs.get("topic", "Photosynthesis")
        grade = inputs.get("grade", 6)
        dialect = inputs.get("dialect", "Telangana Telugu")
        story_mode = inputs.get("story_mode", "modern")

        prompt = self.prompt_template.format(
            topic=topic,
            grade=grade,
            dialect=dialect,
            story_mode=story_mode
        )

        result = self.llm.invoke(prompt)

        try:
            return json.loads(result.content)
        except json.JSONDecodeError:
            return {
                "error": "Story generation failed due to invalid JSON output.",
                "raw_response": result.content
            }
