"""
Crew: VisualAgent Orchestration

This crew manages the VisualAgent responsible for generating age-appropriate visuals (e.g., cartoons, diagrams)
based on lesson topics and dialects.

Flow:
- Triggered after LessonPlannerAgent finishes lesson generation.
- Generates images or illustrations aligned with the topic and student age group.
  
🧵 Parallelism Note:
- Runs in parallel with QuizAgent and StoryTellerAgent crews to speed up multimodal content creation.
- Ensures teacher dashboard receives quiz, story, and visuals simultaneously.

Execution:
- Single agent and task executed sequentially within this crew.

Inputs:
- topic (str): Lesson topic (e.g., "Photosynthesis")
- age_group (str): Target age range (e.g., "6–10 years")
- dialect (str): Language variant (e.g., "Telangana Telugu")
- visual_type (str): Visual style (e.g., "cartoon", "diagram")

Output:
- Visual content metadata or links
"""

from crewflows import Crew
from agents.visual_agent import visual_agent
from tasks.visual_generation_task import generate_visual_task
from tools.visual_generation_tool import VisualGenerationTool

from pydantic import BaseModel, Field, ValidationError
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(levelname)s — %(message)s")
logger = logging.getLogger(__name__)

visual_tool = VisualGenerationTool()
visual_agent.tools = [visual_tool]
visual_agent.allow_delegation = False

crew_visual = Crew(
    agents=[visual_agent],
    tasks=[generate_visual_task],
    process="sequential",
    verbose=True,
    full_output=True
)

class VisualInput(BaseModel):
    topic: str = Field(..., min_length=1)
    age_group: str = Field(..., min_length=1)
    dialect: str = Field(..., min_length=1)
    visual_type: str = Field(..., regex="^(cartoon|diagram|photo|infographic)$")

def run_visual_crew(topic: str, age_group: str, dialect: str, visual_type: str):
    try:
        inputs = VisualInput(topic=topic, age_group=age_group, dialect=dialect, visual_type=visual_type)
        logger.info(f"Validated inputs: {inputs.dict()}")
        result = crew_visual.run(inputs=inputs.dict())
        logger.info("Visual Agent completed successfully")
        return result
    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        return {"error": "Invalid input", "details": ve.errors()}
    except Exception as e:
        logger.error(f"Execution error: {e}")
        return {"error": "Execution failed", "details": str(e)}

if __name__ == "__main__":
    output = run_visual_crew("Photosynthesis", "6–10 years", "Telangana Telugu", "cartoon")
    print(output)
