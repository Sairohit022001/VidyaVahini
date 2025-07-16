"""
Crew: StoryTellerAgent Orchestration

This crew runs the StoryTellerAgent to generate culturally and linguistically relevant stories based on the lesson topic.
It takes topic, grade level, dialect, and desired story mode (e.g., moral, mythological) to create engaging narratives.

Flow:
- Triggered after LessonPlannerAgent generates the lesson content.
- Uses structured lesson input to build stories tailored to the grade level and regional context.

🧵 Parallelism Note:
- This crew is intended to run in parallel with QuizAgent and VisualAgent crews after lesson generation.
- This improves response time for multimodal content generation on the teacher dashboard.

Execution:
- One agent (StoryTellerAgent) + one task (generate_story_task) via CrewAI.

Inputs:
- topic (str): Subject or concept (e.g., “Photosynthesis”)
- grade (int): Target grade level (e.g., 5)
- dialect (str): Language variant (e.g., Telangana Telugu)
- story_mode (str): Style of story — one of ['modern', 'moral', 'mythological', 'folk']

Output:
- Structured JSON story content including title, narrative body, characters, and regional adaptation
"""

from crewflows import Crew
from agents.story_teller_agent import story_teller_agent
from tasks.story_teller_tasks import generate_story_task

from pydantic import BaseModel, Field, ValidationError
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(levelname)s — %(message)s")
logger = logging.getLogger(__name__)

story_teller_crew = Crew(
    agents=[story_teller_agent],
    tasks=[generate_story_task],
    verbose=True
)

class StoryTellerInput(BaseModel):
    topic: str = Field(..., min_length=1)
    grade: int = Field(..., ge=1, le=12)
    dialect: str = Field(..., min_length=1)
    story_mode: str = Field(..., regex="^(modern|moral|mythological|folk)$")

def run_story_generation(topic: str, grade: int, dialect: str, story_mode: str):
    try:
        inputs = StoryTellerInput(topic=topic, grade=grade, dialect=dialect, story_mode=story_mode)
        logger.info(f"Validated inputs: {inputs.dict()}")
        result = story_teller_crew.run(inputs=inputs.dict())
        logger.info("Story Teller Agent completed successfully")
        return result
    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        return {"error": "Invalid input", "details": ve.errors()}
    except Exception as e:
        logger.error(f"Execution error: {e}")
        return {"error": "Execution failed", "details": str(e)}

if __name__ == "__main__":
    output = run_story_generation("Photosynthesis", 5, "Telangana Telugu", "modern")
    print(output)
