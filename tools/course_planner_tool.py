from typing import Dict
import json
from tools.utils.retry_handler import retry_on_failure
from tools.utils.logger import setup_logger
from tools.utils.prompt_loader import load_prompt
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

logger = setup_logger("CoursePlannerTool")

class CoursePlannerTool:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.65,
            convert_system_message_to_human=True
        )
        self.prompt_template = PromptTemplate.from_template(load_prompt("course_planner.txt"))

    @retry_on_failure()
    def run(self, inputs: Dict) -> Dict:
        topic = inputs.get("current_topic", "Photosynthesis")
        level = inputs.get("level", "Medium")
        quiz_score = inputs.get("quiz_score", "70")

        logger.info(f"Generating next topic for: {topic}, quiz_score: {quiz_score}")

        prompt = self.prompt_template.format(current_topic=topic, level=level, quiz_score=quiz_score)
        result = self.llm.invoke(prompt)

        try:
            return json.loads(result.content)
        except json.JSONDecodeError:
            logger.error("Invalid JSON received for course planning")
            return {"error": "Course planning failed. Output was not valid JSON.", "raw_response": result.content}
