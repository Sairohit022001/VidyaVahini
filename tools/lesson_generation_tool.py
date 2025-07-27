# tools/lesson_generation_tool.py

from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.schema import HumanMessage
import json
import logging
import os
import re

from .utils.prompt_loader import get_prompt_template
from tools.utils.retry_handler import retry_with_backoff
from tools.utils.logger import get_logger

logger = get_logger(__name__)

class LessonGenerationTool:
    def __init__(self):
        google_api_key = os.getenv("GOOGLE_API_KEY")
        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-2.5-pro",
            temperature=0.7,
            google_api_key=google_api_key,
            convert_system_message_to_human=True
        )
        self.prompt_template = PromptTemplate.from_template(
            get_prompt_template("lesson_generation")
        )

    def clean_llm_json_output(self, raw_text: str) -> str:
        # Remove markdown code fences (```json or ```)
        cleaned = re.sub(r'^```jsons*', '', raw_text.strip())
        cleaned = re.sub(r'^```s*', '', cleaned)
        cleaned = re.sub(r'```$', '', cleaned.strip())

        # Remove any invisible unicode chars - optional (here using ascii-only)
        # Removed the ASCII encoding/decoding line
        # cleaned = cleaned.encode('ascii', 'ignore').decode('ascii')

        return cleaned

    @retry_with_backoff(retries=3, delay=2)
    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        topic = inputs.get("topic", "Photosynthesis")
        level = inputs.get("level", "Medium")
        dialect = inputs.get("dialect", "Telangana Telugu")
        grade = inputs.get("grade", "")  # Default empty string if missing

        prompt = self.prompt_template.format(topic=topic, level=level, dialect=dialect, grade=grade)
        # Corrected the f-string to use triple quotes
        logger.info("""📌 Prompt sent to Gemini:
%s""", prompt)

        if not prompt.strip():
            logger.error("❌ Generated prompt is empty. Cannot send to LLM.")
            return {
                "error": "Generated prompt is empty. Please provide sufficient inputs (topic, level, dialect).",
                "raw_inputs": inputs
            }

        try:
            messages = [HumanMessage(content=prompt)]
            result = self.llm.invoke(messages)

            logger.debug(f"LLM raw result object: {result}")

            response_text = result.content.strip() if hasattr(result, "content") else str(result).strip()
            # Corrected the f-string to use triple quotes
            logger.debug(f"""LLM response_text: {response_text}""")

            cleaned_text = self.clean_llm_json_output(response_text)
            # Corrected the f-string to use triple quotes
            logger.debug(f"""Cleaned LLM output before JSON parse:
{cleaned_text}""")

            parsed = json.loads(cleaned_text)

            logger.info(f"✅ Lesson generated successfully for topic: {topic}")
            return parsed

        except json.JSONDecodeError:
            # Corrected the f-string to use triple quotes
            logger.error("""❌ JSON decoding failed. Raw output:
%s""", result.content if hasattr(result, "content") else str(result))
            return {
                "error": "Invalid JSON response from LLM.",
                "raw_response": result.content if hasattr(result, "content") else str(result)
            }
        except Exception as e:
            logger.exception("🚨 Unexpected error during lesson generation")
            return {
                "error": "Unexpected failure during lesson generation",
                "details": str(e)
            }

# Instantiate only after class fully defined
lesson_tool = LessonGenerationTool()
