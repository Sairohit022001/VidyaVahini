from crewai import Crew
from agents.content_creator_agent import content_creator_agent
from tasks.content_creator_task import content_creator_task

crew_content_creator_flow = Crew(
    agents=[content_creator_agent],
    tasks=[content_creator_task],
    verbose=True,
    process="sequential",
    memory=True
)

content_creator_agent.add_input("LessonPlannerAgent")
content_creator_agent.add_input("TeacherNotes")
content_creator_agent.add_input("MultimodalResearchAgent")

content_creator_agent.add_output("CombinedLessonContent")
content_creator_agent.add_output("UsedTeacherNotes")
content_creator_agent.add_output("FormattedLessonCard")