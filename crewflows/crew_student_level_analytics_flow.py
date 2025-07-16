"""
Module: Student Level Analytics Crew

Description:
    Orchestrates the Student Level Analytics Agent workflow which processes
    individual student performance data, identifies learning gaps, and
    provides personalized recommendations for improvement.

Features:
- Validates student performance data inputs.
- Outputs detailed insights and learning path suggestions per student.
- Includes logging and error management.

Usage:
    Use `run_student_level_analytics_crew()` with student performance data
    to get personalized analytics.
"""

from crewflows import Crew
from agents.student_level_analytics_agent import student_level_analytics_agent
from tasks.student_level_analytics_task import generate_student_analytics_task
from pydantic import BaseModel, ValidationError, Field
from typing import Dict, List
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(levelname)s — %(message)s")
logger = logging.getLogger(__name__)

# Setup crew
student_level_analytics_crew = Crew(
    agents=[student_level_analytics_agent],
    tasks=[generate_student_analytics_task],
    verbose=True,
    process="sequential",
    memory=True
)

# Input/Output mapping (align with task.py + agent.py)
student_level_analytics_agent.add_input("student_performance")
student_level_analytics_agent.add_output("strengths")
student_level_analytics_agent.add_output("weaknesses")
student_level_analytics_agent.add_output("recommendations")
student_level_analytics_agent.add_output("progress_score")

# Define input schema
class StudentPerformanceInput(BaseModel):
    name: str
    scores: Dict[str, float]
    concept_scores: Dict[str, float]

def run_student_level_analytics_crew(student_performance: dict):
    """
    Runs the Student Level Analytics Crew to analyze a single student's performance.

    Parameters:
        student_performance (dict): Must include:
            - name (str)
            - scores (dict of quiz_name: score)
            - concept_scores (dict of concept_name: score)

    Returns:
        dict: Strengths, weaknesses, progress score, and tailored recommendations.
    """
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

# Dev testing
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
