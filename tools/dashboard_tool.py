from typing import Dict
import json
from tools.utils.retry_handler import retry_with_backoff
from tools.utils.logger import get_logger
from tools.utils.prompt_loader import load_prompt
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

logger = get_logger("DashboardTool")

class TeacherDashboardTool:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            temperature=0.5,
            convert_system_message_to_human=True
        )
        self.prompt_template = PromptTemplate.from_template(load_prompt("dashboard_metrics.txt"))

    @retry_with_backoff()
    def run(self, inputs: Dict) -> Dict:
        class_data = inputs.get("class_data", {})

        logger.info("Generating teacher dashboard metrics")
        prompt = self.prompt_template.format(class_data=str(class_data))
        result = self.llm.invoke(prompt)

        try:
            response_text = str(result.content).strip()
        except json.JSONDecodeError:
            logger.error("Invalid JSON received for dashboard tool")
            return {"error": "Dashboard generation failed.", "raw_response": result.content}