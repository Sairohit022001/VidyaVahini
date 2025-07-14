"""
Crew: DashboardAgent Orchestration

This crew manages the DashboardAgent that aggregates data from multiple agents (QuizAgent, SyncAgent)
to generate actionable insights and alerts for teachers and administrators.

Flow:
- Triggered periodically or on-demand to update the dashboard.
- Processes quiz completion, lesson views, and sync status.
- Identifies students at risk of dropout or flagged for attention.

Memory:
- Uses CrewAI memory to persist state and historical trends.

Parallelism:
- Runs asynchronously alongside other crews such as gamification, lesson, and quiz agents
  without blocking the main workflow.

Inputs:
- QuizAgent (dict): Quiz completion and performance metrics
- SyncAgent (dict): Data synchronization status

Outputs:
- QuizCompletionRate (float): Percentage of completed quizzes
- LessonViewRate (float): Percentage of lessons viewed
- DropoutAlertList (list): List of students at risk of dropping out
- FlaggedStudentsList (list): List of students flagged for teacher attention
"""
from crewai import Crew
from agents.dashboard_agent import dashboard_agent
from tasks.dashboard_task import dashboard_task

from pydantic import BaseModel, ValidationError
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(levelname)s — %(message)s")
logger = logging.getLogger(__name__)

crew_dashboard_flow = Crew(
    agents=[dashboard_agent],
    tasks=[dashboard_task],
    verbose=True,
    process="sequential",
    memory=True
)

dashboard_agent.add_input("QuizAgent")
dashboard_agent.add_input("SyncAgent")

dashboard_agent.add_output("QuizCompletionRate")
dashboard_agent.add_output("LessonViewRate")
dashboard_agent.add_output("DropoutAlertList")
dashboard_agent.add_output("FlaggedStudentsList")

class DashboardInput(BaseModel):
    QuizAgent: dict
    SyncAgent: dict

def run_dashboard_crew(quiz_data, sync_data):
    try:
        inputs = DashboardInput(QuizAgent=quiz_data, SyncAgent=sync_data)
        logger.info(f"Validated inputs: {inputs.dict()}")
        result = crew_dashboard_flow.run(inputs=inputs.dict())
        logger.info("Dashboard Agent completed successfully")
        return result
    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        return {"error": "Invalid input", "details": ve.errors()}
    except Exception as e:
        logger.error(f"Execution error: {e}")
        return {"error": "Execution failed", "details": str(e)}

if __name__ == "__main__":
    sample_quiz_data = {"total_quizzes": 100, "completed_quizzes": 85}
    sample_sync_data = {"last_sync": "2025-07-14T12:00:00Z", "sync_status": "success"}

    output = run_dashboard_crew(sample_quiz_data, sample_sync_data)
    print(output)
