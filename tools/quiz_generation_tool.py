from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import json

from tools.utils.prompt_loader import get_prompt_template
from tools.utils.retry_handler import retry_with_backoff
from tools.utils.logger import get_logger

logger = get_logger(__name__)

class QuizGenerationTool:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.6,
            convert_system_message_to_human=True
        )
        self.prompt_template = PromptTemplate.from_template(
            get_prompt_template("quiz_generation")
        )

    @retry_with_backoff(retries=3, delay=2)
    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        topic = inputs.get("topic", "Photosynthesis")
        level = inputs.get("level", "Medium")
        grade = inputs.get("grade", "6")

        prompt = self.prompt_template.format(topic=topic, level=level, grade=grade)

        try:
            result = self.llm.invoke(prompt)
            parsed = json.loads(result.content.strip())
            logger.info(f"✅ Quiz generated for topic: {topic}")
            return parsed

        except json.JSONDecodeError:
            logger.error("❌ Quiz generation JSON decoding failed")
            return {
                "error": "Invalid JSON in quiz output",
                "raw_response": result.content
            }
        except Exception as e:
            logger.exception("🚨 Quiz generation failed")
            return {
                "error": "Unexpected error",
                "details": str(e)
            }

