from crewai import Crew
from agents.dashboard_agent import dashboard_agent
from tasks.dashboard_task import dashboard_task

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