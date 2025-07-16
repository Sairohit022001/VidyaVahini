"""
Module: Content Creator Crew

Description:
    This module sets up and runs the Content Creator Crew, which orchestrates
    the Content Creator Agent workflow. It includes input validation using
    Pydantic, error handling, and logging to ensure robust execution.

Features:
- Validates inputs such as topic, target audience, and language.
- Handles exceptions gracefully with informative error messages.
- Logs important events for debugging and audit trails.

Usage:
    Call the `run_content_creator_crew()` function with the required inputs
    to generate content based on a specified topic and target audience.
"""


from crewflows import Crew
from agents.content_creator_agent import content_creator_agent
from tasks.content_creator_task import content_creator_task

from pydantic import BaseModel, ValidationError
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(levelname)s — %(message)s")
logger = logging.getLogger(__name__)

# Crew setup
crew_content_creator_flow = Crew(
    agents=[content_creator_agent],
    tasks=[content_creator_task],
    verbose=True,
    process="sequential",
    memory=True
)

# Define agent I/O
content_creator_agent.add_input("LessonPlannerAgent")
content_creator_agent.add_input("TeacherNotes")
content_creator_agent.add_input("MultimodalResearchAgent")

content_creator_agent.add_output("CombinedLessonContent")
content_creator_agent.add_output("UsedTeacherNotes")
content_creator_agent.add_output("FormattedLessonCard")

# Input validation schema
class ContentCreatorInput(BaseModel):
    LessonPlannerAgent: dict
    TeacherNotes: dict
    MultimodalResearchAgent: dict

def run_content_creator_crew(lesson_data, teacher_notes, research_data):
    """
    Executes the Content Creator crew with validated inputs.

    Parameters:
        lesson_data (dict): Output from LessonPlannerAgent
        teacher_notes (dict): Teacher's notes input
        research_data (dict): Output from MultimodalResearchAgent

    Returns:
        dict: Result from Content Creator Agent or error details.
    """
    try:
        inputs = ContentCreatorInput(
            LessonPlannerAgent=lesson_data,
            TeacherNotes=teacher_notes,
            MultimodalResearchAgent=research_data
        )
        logger.info(f"Validated inputs: {inputs.dict()}")
        result = crew_content_creator_flow.run(inputs=inputs.dict())
        logger.info("Content Creator Agent completed successfully")
        return result
    except ValidationError as ve:
        logger.error(f"Input validation error: {ve}")
        return {"error": "Invalid input", "details": ve.errors()}
    except Exception as e:
        logger.error(f"Execution error: {e}")
        return {"error": "Execution failed", "details": str(e)}


if __name__ == "__main__":
    # Example usage with dummy data
    sample_lesson_data = {"topic": "Photosynthesis", "concepts": ["Light reaction", "Calvin cycle"]}
    sample_teacher_notes = {"notes": "Focus on real-world examples"}
    sample_research_data = {"papers": ["Paper1", "Paper2"]}

    output = run_content_creator_crew(sample_lesson_data, sample_teacher_notes, sample_research_data)
    print(output)
