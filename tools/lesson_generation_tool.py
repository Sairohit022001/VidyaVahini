# tools/lesson_generation_tool.py

from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import json
import logging

import sys
print(sys.path)


from .utils.prompt_loader import get_prompt_template

from tools.utils.retry_handler import retry_with_backoff
from tools.utils.logger import get_logger

logger = get_logger(__name__)

class LessonGenerationTool:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.7,
            convert_system_message_to_human=True
        )
        self.prompt_template = PromptTemplate.from_template(
            get_prompt_template("lesson_generation")
        )

    @retry_with_backoff(retries=3, delay=2)
    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        topic = inputs.get("topic", "Photosynthesis")
        level = inputs.get("level", "Medium")
        dialect = inputs.get("dialect", "Telangana Telugu")

        prompt = self.prompt_template.format(topic=topic, level=level, dialect=dialect)

        try:
            result = self.llm.invoke(prompt)
            response_text = result.content.strip()

            parsed = json.loads(response_text)
            logger.info(f"✅ Lesson generated for topic: {topic}")
            return parsed

        except json.JSONDecodeError:
            logger.error("❌ JSON decoding failed. Raw output:\n%s", result.content)
            return {
                "error": "Invalid JSON response from LLM.",
                "raw_response": result.content
            }
        except Exception as e:
            logger.exception("🚨 Unexpected error during lesson generation")
            return {
                "error": "Unexpected failure during lesson generation",
                "details": str(e)
            }
