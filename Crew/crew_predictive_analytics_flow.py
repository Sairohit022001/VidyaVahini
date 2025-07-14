"""
Module: Predictive Analytics Crew

Description:
    This module orchestrates the Predictive Analytics Agent, which analyzes quiz
    and performance data to generate class-level and student-level insights.
    It identifies weak areas, top performers, trends across quizzes, and suggests
    chapters and concepts to focus on or re-explain.

Features:
- Validates input quiz results data.
- Provides aggregated analytics such as average scores and recommendations.
- Handles errors and logs detailed execution information.

Usage:
    Call `run_predictive_analytics_crew()` with quiz results data to receive
    analytics summaries and student-level insights.
"""

from crewai import Crew
from agents.predictive_analytics_agent import predictive_analytics_agent
from tasks.predictive_analytics_task import generate_class_analytics_task

from pydantic import BaseModel, ValidationError
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(levelname)s — %(message)s")
logger = logging.getLogger(__name__)

# Setup Crew
predictive_analytics_crew = Crew(
    agents=[predictive_analytics_agent],
    tasks=[generate_class_analytics_task],
    verbose=True,
    process="sequential",
    memory=True
)

predictive_analytics_agent.add_input("quiz_results")
predictive_analytics_agent.add_output("average_score")
predictive_analytics_agent.add_output("top_performers")
predictive_analytics_agent.add_output("weak_areas")
predictive_analytics_agent.add_output("recommendations")

# Input validation schema
class QuizResultsInput(BaseModel):
    quiz_results: dict  # You can define a more detailed schema if needed

def run_predictive_analytics_crew(quiz_results: dict):
    """
    Runs the Predictive Analytics Crew workflow to analyze quiz data.

    Parameters:
        quiz_results (dict): Nested dictionary containing quiz results per student and quiz.

    Returns:
        dict: Analytics including average scores, top performers, weak areas,
              and recommendations, or error details.
    """
    try:
        inputs = QuizResultsInput(quiz_results=quiz_results)
        logger.info(f"Validated inputs for quiz results analytics")
        result = predictive_analytics_crew.run(inputs=inputs.dict())
        logger.info("Predictive Analytics Agent completed successfully")
        return result
    except ValidationError as ve:
        logger.error(f"Input validation failed: {ve}")
        return {"error": "Invalid input", "details": ve.errors()}
    except Exception as e:
        logger.error(f"Execution error: {e}")
        return {"error": "Execution failed", "details": str(e)}

if __name__ == "__main__":
    sample_quiz_results = {
        "student_1": {"quiz_1": 85, "quiz_2": 78},
        "student_2": {"quiz_1": 90, "quiz_2": 88},
        # ...
    }
    output = run_predictive_analytics_crew(sample_quiz_results)
    print(output)
