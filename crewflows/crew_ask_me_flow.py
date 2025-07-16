"""
Module: Ask Me Crew

Description:
    This module configures and runs the Ask Me Crew, managing the Ask Me Agent
    that responds to user questions. It provides structured input validation,
    comprehensive error handling, and detailed logging for reliability.

Features:
- Validates user question, context, and language inputs.
- Provides clear error messages in case of invalid inputs or execution errors.
- Logs key steps to facilitate monitoring and debugging.

Usage:
    Use the `run_ask_me_crew()` function to process user questions and retrieve
    answers, optionally including context to improve response relevance.
"""
from crewflows.core import Crew

from agents.ask_me_agent import ask_me_agent
from tasks.ask_me_task import ask_question_task


from dotenv import load_dotenv
load_dotenv()

from pydantic import BaseModel, Field, ValidationError
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(levelname)s — %(message)s")
logger = logging.getLogger(__name__)

# Crew setup
ask_me_crew = Crew(
    agents=[ask_me_agent],
    tasks=[ask_question_task],
    verbose=True,
    process="sequential",  # single agent process, so sequential is appropriate
)

# Input validation schema
class AskMeInput(BaseModel):
    question: str = Field(..., min_length=1, description="User's question")
    context: str = Field(default="", description="Optional context or reference material")

def run_ask_me_flow(question: str, context: str = ""):
    """
    Entry point for AskMeAgent to answer a classroom doubt.

    Parameters:
        question (str): The user's query.
        context (str, optional): Lesson context or reference material.

    Returns:
        dict: JSON-compatible answer with follow-up and metadata or error info.
    """
    try:
        inputs = AskMeInput(question=question, context=context)
        logger.info(f"Validated inputs: {inputs.dict()}")
        result = ask_me_crew.run(inputs=inputs.dict())
        logger.info("Ask Me Agent completed successfully")
        return result
    except ValidationError as ve:
        logger.error(f"Input validation error: {ve}")
        return {"error": "Invalid input", "details": ve.errors()}
    except Exception as e:
        logger.error(f"Execution error: {e}")
        return {"error": "Execution failed", "details": str(e)}

if __name__ == "__main__":
    example_question = "What is photosynthesis?"
    example_context = "Lesson about plant biology."
    output = run_ask_me_flow(example_question, example_context)
    print(output)