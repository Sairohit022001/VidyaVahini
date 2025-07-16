"""
Crew: CoursePlannerAgent Orchestration

This crew runs the CoursePlannerAgent to generate or update course plans based on student performance,
current topics, and quiz scores.

Flow:
- Triggered after quiz completion or lesson updates.
- Uses CoursePlannerTool to analyze performance and suggest personalized course paths or topics to focus.

Parallelism:
- Can run asynchronously alongside lesson generation, quiz, and story generation crews to optimize responsiveness.

Inputs:
- current_topic (str): The topic currently studied by the student
- quiz_score (int): The student’s score on the related quiz

Outputs:
- Updated course plan recommendations tailored to student progress
"""

from crewflows import Crew
from agents.course_planner_agent import course_planner_agent
from tasks.course_planner_tasks import generate_course_plan_task
from tools.course_planner_tool import CoursePlannerTool

from pydantic import BaseModel, Field, ValidationError
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)
logger = logging.getLogger(__name__)

# Input validation schema
class CoursePlannerInput(BaseModel):
    current_topic: str = Field(..., min_length=1, description="Current topic being studied")
    quiz_score: int = Field(..., ge=0, le=100, description="Quiz score as a percentage (0-100)")

# Tool setup
course_planner_tool = CoursePlannerTool()
generate_course_plan_task.run = course_planner_tool.run

# Crew
crew_course_planner = Crew(
    agents=[course_planner_agent],
    tasks=[generate_course_plan_task],
    verbose=True
)

def run_course_planner_crew(current_topic: str, quiz_score: int):
    try:
        validated_inputs = CoursePlannerInput(current_topic=current_topic, quiz_score=quiz_score)
        logger.info("Input validation passed")

        inputs = validated_inputs.dict()
        logger.info(f"Running Course Planner with inputs: {inputs}")

        result = crew_course_planner.kickoff(inputs=inputs)

        logger.info("Course Planner Agent executed successfully")
        return result

    except ValidationError as ve:
        logger.error(f"Input validation error: {ve}")
        return {"error": "Invalid input", "details": ve.errors()}

    except Exception as e:
        logger.error(f"Unexpected error during crew execution: {e}")
        return {"error": "Execution failed", "details": str(e)}

if __name__ == "__main__":
    output = run_course_planner_crew("Photosynthesis", 68)
    print("\n[🗂️ COURSE PLANNER OUTPUT]\n")
    print(output)
