"""
Crew: QuizAgent Orchestration

This crew runs the QuizAgent to generate context-aware quizzes based on the structured lesson content.
It takes topic, level, dialect, and optionally a story context, and produces multiple-choice questions (MCQs).

Flow:
- Triggered after LessonPlannerAgent generates lesson output.
- Uses QuizGenerationTool (LLM-based) to produce questions aligned with the topic and story.
- Designed to be stateless and parallelizable with StoryTellerAgent and VisualAgent.

Execution:
- One agent (QuizAgent) + one task (generate_quiz_task) executed via CrewAI.

Inputs:
- topic (str): Lesson topic
- level (str): Difficulty level
- dialect (str): Language dialect (e.g., Telangana Telugu)
- story_context (str): Optional story for contextual question generation

Output:
- List of multiple-choice questions in structured format
"""
from crewflows import Crew
from agents.quiz_agent import quiz_agent
from tasks.quiz_tasks import generate_quiz_task
from tools.quiz_generation_tool import QuizGenerationTool

from pydantic import BaseModel, Field, ValidationError
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(levelname)s — %(message)s")
logger = logging.getLogger(__name__)

quiz_tool = QuizGenerationTool()
generate_quiz_task.run = quiz_tool.run

quiz_crew = Crew(
    agents=[quiz_agent],
    tasks=[generate_quiz_task],
    verbose=True,
    process_name="Quiz Flow Pipeline"
)

class QuizInput(BaseModel):
    topic: str = Field(..., min_length=1)
    level: str = Field(..., min_length=1)
    dialect: str = Field(..., min_length=1)
    story_context: str = Field(default="")

def run_quiz_crew(topic: str, level: str, dialect: str, story_context: str = ""):
    try:
        inputs = QuizInput(topic=topic, level=level, dialect=dialect, story_context=story_context)
        logger.info(f"Validated inputs: {inputs.dict()}")
        result = quiz_crew.run(inputs=inputs.dict())
        logger.info("Quiz Agent completed successfully")
        return result
    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        return {"error": "Invalid input", "details": ve.errors()}
    except Exception as e:
        logger.error(f"Execution error: {e}")
        return {"error": "Execution failed", "details": str(e)}

if __name__ == "__main__":
    output = run_quiz_crew("Photosynthesis", "Medium", "Telangana Telugu", "Story about a village farmer and crops")
    print(output)
