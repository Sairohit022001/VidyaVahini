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

from crewai import Crew
from agents.student_level_analytics_agent import student_level_analytics_agent
from tasks.student_level_analytics_task import student_level_analytics_task

from pydantic import BaseModel, ValidationError
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(levelname)s — %(message)s")
logger = logging.getLogger(__name__)

# Crew setup
student_level_analytics_crew = Crew(
    agents=[student_level_analytics_agent],
    tasks=[student_level_analytics_task],
    verbose=True,
    process="sequential",
    memory=True
)

student_level_analytics_agent.add_input("student_performance_data")
student_level_analytics_agent.add_output("learning_gaps")
student_level_analytics_agent.add_output("personalized_recommendations")
student_level_analytics_agent.add_output("progress_reports")

# Input validation schema
class StudentPerformanceInput(BaseModel):
    student_performance_data: dict  # Define detailed schema if possible

def run_student_level_analytics_crew(student_performance_data: dict):
    """
    Runs Student Level Analytics Crew for personalized student insights.

    Parameters:
        student_performance_data (dict): Performance data per student.

    Returns:
        dict: Learning gaps, recommendations, progress reports, or errors.
    """
    try:
        inputs = StudentPerformanceInput(student_performance_data=student_performance_data)
        logger.info("Validated student performance input")
        result = student_level_analytics_crew.run(inputs=inputs.dict())
        logger.info("Student Level Analytics Agent completed successfully")
        return result
    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        return {"error": "Invalid input", "details": ve.errors()}
    except Exception as e:
        logger.error(f"Execution error: {e}")
        return {"error": "Execution failed", "details": str(e)}

if __name__ == "__main__":
    sample_student_data = {
        "student_1": {"quiz_1": 75, "quiz_2": 65},
        "student_2": {"quiz_1": 90, "quiz_2": 95}
    }
    output = run_student_level_analytics_crew(sample_student_data)
    print(output)
