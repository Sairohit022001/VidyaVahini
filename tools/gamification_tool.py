from typing import Dict
import json
from tools.utils.retry_handler import retry_with_backoff
from tools.utils.logger import get_logger
from tools.utils.prompt_loader import load_prompt
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

logger = get_logger("GamificationTool")

class GamificationTool:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.6,
            convert_system_message_to_human=True
        )
        self.prompt_template = PromptTemplate.from_template(load_prompt("gamification.txt"))

    @retry_with_backoff()
    def run(self, inputs: Dict) -> Dict:
        student_data = inputs.get("student_data", {})
        logger.info("Generating gamification metrics")

        prompt = self.prompt_template.format(student_data=str(student_data))
        result = self.llm.invoke(prompt)

        try:
            response_text = str(result.content).strip()
        except json.JSONDecodeError:
            logger.error("Invalid JSON from LLM for gamification")
            return {"error": "Gamification generation failed.", "raw_response": result.content}