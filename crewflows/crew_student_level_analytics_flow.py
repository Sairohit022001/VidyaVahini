from crewflows import Crew
from agents.student_level_analytics_agent import student_level_analytics_agent
from pydantic import BaseModel, ValidationError
from typing import Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StudentPerformanceInput(BaseModel):
    name: str
    scores: Dict[str, float]
    concept_scores: Dict[str, float]

student_level_analytics_crew = Crew(
    agents=[student_level_analytics_agent],
    tasks=student_level_analytics_agent.tasks,
    verbose=True,
    process="sequential",
    memory=True
)

def run_student_level_analytics_crew(student_performance: dict):
    try:
        inputs = StudentPerformanceInput(**student_performance)
        logger.info("✅ Input validation successful.")
        result = student_level_analytics_crew.run(inputs={"student_performance": inputs.dict()})
        logger.info("🎯 Student Analytics completed successfully.")
        return result
    except ValidationError as ve:
        logger.error(f"❌ Input validation failed: {ve}")
        return {"error": "Invalid input", "details": ve.errors()}
    except Exception as e:
        logger.error(f"❌ Execution failed: {e}")
        return {"error": "Execution failed", "details": str(e)}

if __name__ == "__main__":
    sample_input = {
        "name": "Sita",
        "scores": {
            "quiz_1": 85,
            "quiz_2": 70
        },
        "concept_scores": {
            "Photosynthesis": 82,
            "Food Chain": 48,
            "Water Cycle": 90
        }
    }

    output = run_student_level_analytics_crew(sample_input)
    print("\n[📚 STUDENT ANALYTICS RESULT]")
    print(output)

