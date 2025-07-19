from typing import Dict, Any
import json

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

from tools.utils.prompt_loader import get_prompt_template
from tools.utils.retry_handler import retry_with_backoff
from tools.utils.logger import get_logger
from tools.base import BaseTool

logger = get_logger(__name__)

class VisualGenerationTool(BaseTool):
    def __init__(self):
        try:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-pro",
                temperature=0.65,
                convert_system_message_to_human=True
            )
            self.prompt_template = PromptTemplate.from_template(self._get_visual_prompt())
        except Exception as e:
            logger.exception("❌ Failed to initialize VisualGenerationTool")
            raise RuntimeError("Initialization failed in VisualGenerationTool") from e

    def _get_visual_prompt(self) -> str:
        return """
You are a visual teaching assistant helping students learn through image-based prompts.

🎯 Task: Generate 3 detailed **visual scene descriptions** that can be used to create educational illustrations for the concept: "{concept}"  
🎓 Grade Level: {grade}  
🗣️ Dialect: {dialect}

Each visual should:
- Be described clearly in simple language suitable for the grade level.
- Mention setting, key elements, actions, and expressions if any.
- Avoid abstract text — focus on what should be *seen* in the image.

✅ Return the output in the following JSON format (without any markdown):

{
  "visual_prompts": [
    {
      "title": "Scene Title 1",
      "description": "A clear, detailed description of the first image"
    },
    {
      "title": "Scene Title 2",
      "description": "A clear, detailed description of the second image"
    },
    {
      "title": "Scene Title 3",
      "description": "A clear, detailed description of the third image"
    }
  ]
}
"""

    @retry_with_backoff(retries=3, delay=2)
    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        concept = inputs.get("concept", "Photosynthesis")
        grade = inputs.get("grade", "6")
        dialect = inputs.get("dialect", "Telangana Telugu")

        prompt = self.prompt_template.format(
            concept=concept,
            grade=grade,
            dialect=dialect
        )

        try:
            result = self.llm.invoke(prompt)
            content = result.content.strip()

            # Handle markdown-wrapped output
            if content.startswith("```json"):
                content = content.replace("```json", "").replace("```", "").strip()
            elif content.startswith("```"):
                content = content.replace("```", "").strip()

            parsed = json.loads(content)
            logger.info(f"✅ Visual prompts generated successfully for concept: {concept}")
            return parsed

        except json.JSONDecodeError:
            logger.error("❌ JSON decoding failed in VisualGenerationTool")
            return {
                "error": "Visual generation failed due to JSON format issue.",
                "raw_response": result.content
            }

        except Exception as e:
            logger.exception("🚨 Unexpected error during visual generation")
            return {
                "error": "Unexpected error occurred.",
                "details": str(e)
            }
