# tools/lesson_generation_tool.py

from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.schema import HumanMessage
import json
import logging
import sys

from .utils.prompt_loader import get_prompt_template
from tools.utils.retry_handler import retry_with_backoff
from tools.utils.logger import get_logger

logger = get_logger(__name__)

import re

class LessonGenerationTool:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-2.5-pro",
            temperature=0.7,
            convert_system_message_to_human=True
        )
        self.prompt_template = PromptTemplate.from_template(
            get_prompt_template("lesson_generation")
        )

    def clean_llm_json_output(self, raw_text: str) -> str:
        # Remove markdown code fences (```json or ```)
        cleaned = re.sub(r'^```json\s*', '', raw_text.strip())
        cleaned = re.sub(r'^```\s*', '', cleaned)
        cleaned = re.sub(r'```$', '', cleaned.strip())

        # Remove any invisible unicode chars - optional (here using ascii-only)
        cleaned = cleaned.encode('ascii', 'ignore').decode('ascii')

        return cleaned

    @retry_with_backoff(retries=3, delay=2)
    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        topic = inputs.get("topic", "Photosynthesis")
        level = inputs.get("level", "Medium")
        dialect = inputs.get("dialect", "Telangana Telugu")

        prompt = self.prompt_template.format(topic=topic, level=level, dialect=dialect)
        print("📌 Prompt sent to Gemini:")
        print(prompt)

        if not prompt.strip():
            logger.error("❌ Generated prompt is empty. Cannot send to LLM.")
            return {
                "error": "Generated prompt is empty. Please provide sufficient inputs (topic, level, dialect).",
                "raw_inputs": inputs
            }

        try:
            messages = [HumanMessage(content=prompt)]
            result = self.llm.invoke(messages)

            response_text = result.content.strip() if hasattr(result, "content") else str(result).strip()
            cleaned_text = self.clean_llm_json_output(response_text)
            parsed = json.loads(cleaned_text)

            logger.info(f"✅ Lesson generated for topic: {topic}")
            return parsed

        except json.JSONDecodeError:
            logger.error("❌ JSON decoding failed. Raw output:")
            logger.error("%s", result.content)
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


# ✅ Only instantiate after class is fully defined
lesson_tool = LessonGenerationTool()
