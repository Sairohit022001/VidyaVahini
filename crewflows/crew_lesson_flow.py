from crewflows import Crew
from agents.lesson_planner_agent import lesson_planner_agent
from tasks.lesson_planner_tasks import lesson_generation_task
from tools.lesson_planner_tool import LessonPlannerTool

from pydantic import BaseModel, Field, ValidationError
import logging

"""
Crew: LessonPlannerAgent Orchestration

This crew is responsible for generating structured lesson plans using the LessonPlannerAgent.
It runs the task `lesson_generation_task` sequentially using the provided inputs: topic, level, and dialect.

Flow:
- Triggered when a teacher selects a topic
- Runs LessonPlannerAgent → outputs lesson JSON (intended for downstream use by QuizAgent, StoryTellerAgent, VisualAgent)

Execution:
- Currently uses process='sequential' as there's only one task-agent pair.
- Designed to be expandable into hierarchical or async workflows in the future.

Inputs:
- topic (str): Subject or concept selected by teacher
- level (str): Grade level
- dialect (str): Regional language/dialect (e.g., Telangana Telugu)

Outputs:
- Structured lesson content conforming to LessonOutputSchema
"""

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(levelname)s — %(message)s")
logger = logging.getLogger(__name__)

# Tool setup
lesson_planner_tool = LessonPlannerTool()
lesson_generation_task.run = lesson_planner_tool.run

# Crew setup
lesson_crew = Crew(
    agents=[lesson_planner_agent],
    tasks=[lesson_generation_task],
    verbose=True,
)

# Input schema
class LessonPlannerInput(BaseModel):
    topic: str = Field(..., min_length=1)
    level: str = Field(..., min_length=1)
    dialect: str = Field(..., min_length=1)

def run_lesson_crew(topic: str, level: str, dialect: str):
    try:
        inputs = LessonPlannerInput(topic=topic, level=level, dialect=dialect)
        logger.info(f"Validated inputs: {inputs.dict()}")
        result = lesson_crew.kickoff(inputs=inputs.dict())
        logger.info("Lesson Planner Agent completed successfully")
        return result
    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        return {"error": "Invalid input", "details": ve.errors()}
    except Exception as e:
        logger.error(f"Execution error: {e}")
        return {"error": "Execution failed", "details": str(e)}

if __name__ == "__main__":
    output = run_lesson_crew("Photosynthesis", "5th Grade", "Telangana Telugu")
    print(output)
