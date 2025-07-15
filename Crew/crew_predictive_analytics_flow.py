"""
Module: Predictive Analytics Crew

Description:
    This module orchestrates the Predictive Analytics Agent, which analyzes
    quiz and performance data to generate class-level insights only.
    It identifies weak areas, top performers, and average score, and suggests
    chapters and concepts to re-explain in future lessons.

Features:
- Validates input quiz results data.
- Provides aggregate analytics like average score and weak topics.
- Handles errors and logs execution details for debugging.

Usage:
    Call `run_predictive_analytics_crew()` with quiz results to get structured
    class-level analytics report.
"""

from crewai import Crew
from agents.predictive_analytics_agent import predictive_analytics_agent
from tasks.predictive_analytics_task import generate_class_analytics_task
from pydantic import BaseModel, Field, ValidationError
import logging
from typing import List, Dict

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(levelname)s — %(message)s")
logger = logging.getLogger(__name__)

# Crew definition
predictive_analytics_crew = Crew(
    agents=[predictive_analytics_agent],
    tasks=[generate_class_analytics_task],
    verbose=True,
    process="sequential",
    memory=True
)

# Outputs based on class-level analytics task
predictive_analytics_agent.add_input("quiz_results")
predictive_analytics_agent.add_output("average_score")
predictive_analytics_agent.add_output("top_performers")
predictive_analytics_agent.add_output("weak_areas")
predictive_analytics_agent.add_output("lesson_plan_suggestions")

# Input schema aligned with tool expectations
class StudentScore(BaseModel):
    name: str
    score: float

class QuizResultsInput(BaseModel):
    students: List[StudentScore]
    weak_areas: List[str] = Field(default=[])

# Crew runner function
def run_predictive_analytics_crew(quiz_results: dict):
    """
    Runs the Predictive Analytics Crew to analyze quiz results.

    Parameters:
        quiz_results (dict): Must include `students` (list of dicts with name, score)
                             and optionally `weak_areas` (list of strings)

    Returns:
        dict: Class-level analytics including average score, top performers, weak areas,
              and suggested lesson topics.
    """
    try:
        validated = QuizResultsInput(**quiz_results)
        logger.info("✅ Input validation successful.")
        result = predictive_analytics_crew.run(inputs={"quiz_results": validated.dict()})
        logger.info("🎯 Predictive Analytics completed successfully.")
        return result
    except ValidationError as ve:
        logger.error(f"❌ Input validation failed: {ve}")
        return {"error": "Invalid input", "details": ve.errors()}
    except Exception as e:
        logger.error(f"❌ Unexpected error during execution: {e}")
        return {"error": "Execution failed", "details": str(e)}

# Test runner
if __name__ == "__main__":
    sample_input = {
        "students": [
            {"name": "Ravi", "score": 88},
            {"name": "Anjali", "score": 93},
            {"name": "Ayaan", "score": 76}
        ],
        "weak_areas": ["Photosynthesis", "Food Chain"]
    }

    output = run_predictive_analytics_crew(sample_input)
    print("\n[📊 CLASS ANALYTICS OUTPUT]")
    print(output)
