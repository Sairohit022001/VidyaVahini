import json
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from tools.utils.prompt_loader import get_prompt_template
from tools.utils.retry_handler import retry_with_backoff
from tools.utils.logger import get_logger

logger = get_logger(__name__)

class QuizGenerationTool:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            temperature=0.6,
            convert_system_message_to_human=True
        )
        # Load prompt template named "quiz_agent" (make sure this exists in your prompt utils)
        self.prompt_template = PromptTemplate.from_template(
            get_prompt_template("quiz_agent")
        )

    def run(self, inputs: dict) -> dict:
        """
        Generate quiz JSON from inputs by calling the LLM with a formatted prompt.
        Returns parsed quiz JSON or fallback on error.
        """
        try:
            # Format prompt with input data
            prompt_text = self.prompt_template.format(**inputs)

            # Call the LLM's synchronous predict method to get raw text response
            response_text = self.llm.predict(prompt_text)

            # Debug: log or print response type and sample (optional)
            logger.debug(f"LLM response type: {type(response_text)}")
            logger.debug(f"LLM response text (truncated): {response_text[:200]}")

            # Parse the JSON output from the model response
            quiz_data = json.loads(response_text)

            # Validate essential keys in quiz_data
            required_keys = ["quiz_json", "adaptive_quiz_set", "retry_feedback_report"]
            missing_keys = [k for k in required_keys if k not in quiz_data]
            if missing_keys:
                logger.warning(f"QuizGenerationTool.run() output missing keys: {missing_keys}")
                return self.get_fallback()

            return quiz_data

        except json.JSONDecodeError as jde:
            logger.error(f"JSON decode error in QuizGenerationTool.run(): {jde}")
        except Exception as e:
            logger.error(f"Unexpected error in QuizGenerationTool.run(): {e}", exc_info=True)

        # Return fallback quiz in case of any failure
        return self.get_fallback()

    def get_fallback(self) -> dict:
        """
        Returns a default fallback quiz JSON in case generation fails.
        """
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
            "adaptive_quiz_set": {
                "easy": [],
                "medium": [],
                "hard": []
            },
            "retry_feedback_report": {}
        }
