from crewai import Crew
from agents.gamification_agent import gamification_agent
from tasks.gamification_task import gamification_task

crew_gamification_flow = Crew(
    agents=[gamification_agent],
    tasks=[gamification_task],
    verbose=True,
    process="sequential",
    memory=True
)

gamification_agent.add_input("QuizAgent")
gamification_agent.add_input("LessonPlannerAgent")
gamification_agent.add_input("ContentCreatorAgent")

gamification_agent.add_output("XPDistribution")
gamification_agent.add_output("BadgesEarned")
gamification_agent.add_output("LeaderboardData")