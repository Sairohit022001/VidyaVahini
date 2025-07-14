from crewai import Crew
from agents.course_planner_agent import course_planner_agent
from tasks.course_planner_tasks import generate_course_plan_task
from tools.course_planner_tool import CoursePlannerTool

# Tool setup
course_planner_tool = CoursePlannerTool()
generate_course_plan_task.run = course_planner_tool.run

# Crew
crew_course_planner = Crew(
    agents=[course_planner_agent],
    tasks=[generate_course_plan_task],
    verbose=True
)

if __name__ == "__main__":
    # Sample call for dev testing
    output = crew_course_planner.kickoff(inputs={
        "current_topic": "Photosynthesis",
        "quiz_score": 68
    })
    print(output)
