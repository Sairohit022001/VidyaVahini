from typing import Dict
import json
from tools.utils.retry_handler import retry_with_backoff
from tools.utils.logger import get_logger
from tools.utils.prompt_loader import load_prompt
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

logger = get_logger("CoursePlannerTool")

class CoursePlannerTool:
    def __init__(self):
        # Initialize the Gemini 2.5 Pro LLM with moderate creativity
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            temperature=0.65,
            convert_system_message_to_human=True
        )
        # Load the prompt template from file course_planner.txt
        self.prompt_template = PromptTemplate.from_template(load_prompt("course_planner.txt"))

    @retry_with_backoff()
    def run(self, inputs: Dict) -> Dict:
        # Extract inputs with defaults
        topic = inputs.get("current_topic", "Photosynthesis")
        level = inputs.get("level", "Medium")
        quiz_score = inputs.get("quiz_score", "70")

        logger.info(f"Generating next topic for: {topic}, quiz_score: {quiz_score}")

        # Format the prompt with current context
        prompt = self.prompt_template.format(current_topic=topic, level=level, quiz_score=quiz_score)
        
        # Call LLM to generate result
        result = self.llm.invoke(prompt)

        try:
            # Parse or clean output text
            response_text = str(result.content).strip()
            # Try to parse JSON if expected (optional, depends on prompt design)
            response_json = json.loads(response_text)
            return response_json
        except json.JSONDecodeError:
            logger.error("Invalid JSON received for course planning")
            # Return error info along with raw text
            return {"error": "Course planning failed. Output was not valid JSON.", "raw_response": response_text}
