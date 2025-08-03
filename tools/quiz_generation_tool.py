import json
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from tools.utils.prompt_loader import get_prompt_template
from tools.utils.logger import get_logger

logger = get_logger(__name__)

class QuizGenerationTool:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            temperature=0.6,
            convert_system_message_to_human=True
        )
        # Make sure your "quiz_agent" template uses only named keys!
        self.prompt_template = PromptTemplate.from_template(
            get_prompt_template("quiz_agent")
        )

    def run(self, inputs: dict) -> dict:
        try:
            # Log keys for debugging
            logger.debug(f"Quiz input keys: {list(inputs.keys())}")
            # Ensure all required keys are present
            required_keys = self.prompt_template.input_variables
            for key in required_keys:
                if key not in inputs:
                    logger.warning(f"Missing key for quiz prompt: '{key}', adding empty string for formatting safety.")
                    inputs.setdefault(key, "")
            # Format prompt with named keys only!
            prompt_text = self.prompt_template.format(**inputs)
            response_text = self.llm.predict(prompt_text)
            logger.debug(f"LLM response text (truncated): {response_text[:200]}")
            quiz_data = json.loads(response_text)
            for needed in ["quiz_json", "adaptive_quiz_set", "retry_feedback_report"]:
                if needed not in quiz_data:
                    logger.warning(f"Missing key '{needed}' in quiz result")
                    return self.get_fallback()
            return quiz_data
        except json.JSONDecodeError as jde:
            logger.error(f"JSON decode error: {jde}")
        except Exception as e:
            logger.error(f"QuizGenerationTool error: {e}", exc_info=True)
        return self.get_fallback()

    def get_fallback(self) -> dict:
        return {
            "quiz_json": {
                "questions": [
                    {
                        "question_text": "What is photosynthesis?",
                        "options": [
                            "Process of making food by plants",
                            "Breathing process",
                            "Water cycle",
                            "Seed germination"
                        ],
                        "correct_answer": "Process of making food by plants",
                        "explanation": "Photosynthesis is the process by which plants make food using sunlight."
                    }
                ],
                "format_type": "MCQ",
                "topic": "Default Topic",
                "grade_level": "Unknown",
                "total_marks": 1,
                "dialect_adapted": False
            },
            "adaptive_quiz_set": {"easy": [], "medium": [], "hard": []},
            "retry_feedback_report": {}
        }
