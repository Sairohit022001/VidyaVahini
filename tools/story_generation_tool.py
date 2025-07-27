# tools/story_generation_tool.py

from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import json

from tools.utils.prompt_loader import get_prompt_template
from tools.utils.retry_handler import retry_with_backoff
from tools.utils.logger import get_logger

logger = get_logger(__name__)

import re

class StoryGenerationTool:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            temperature=0.75,
            convert_system_message_to_human=True
        )
        self.prompt_template = PromptTemplate.from_template(
            get_prompt_template("story_teller")
        )

    def clean_llm_json_output(self, raw_text: str) -> str:
        # Strip markdown code fences like ```json and ```
        cleaned = re.sub(r'^```jsons*', '', raw_text.strip())
        cleaned = re.sub(r'^```s*', '', cleaned)
        cleaned = re.sub(r'```$', '', cleaned.strip())
        # Optional: remove invisible unicode chars
        # Removed the ASCII encoding/decoding line
        # cleaned = cleaned.encode('ascii', 'ignore').decode('ascii')
        return cleaned

    @retry_with_backoff(retries=3, delay=2)
    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        topic = inputs.get("topic", "Photosynthesis")
        grade = inputs.get("grade", "6")
        dialect = inputs.get("dialect", "Telangana Telugu")

        prompt = self.prompt_template.format(topic=topic, grade=grade, dialect=dialect)

        try:
            result = self.llm.invoke(prompt)
            raw_response = result.content.strip()
            cleaned_response = self.clean_llm_json_output(raw_response)

            try:
                parsed = json.loads(cleaned_response)
                logger.info(f"✅ Story generated for topic: {topic}")
                return parsed

            except json.JSONDecodeError as e:
                logger.error(f"❌ JSONDecodeError in story output: {e}")
                logger.error(f"Raw response: {raw_response}")
                # Return a structured error response that includes the problematic raw_response
                return {
                    "error": "Story generation failed due to invalid JSON output from LLM.",
                    "details": str(e),
                    "raw_response": raw_response # Include raw response for debugging
                }

        except Exception as e:
            logger.exception("🚨 Story generation failed")
            # Return a structured error response for other exceptions
            return {
                "error": "Unexpected failure during story generation.",
                "details": str(e)
            }
