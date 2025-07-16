from crewai import Agent
from crewai.memory import MemoryHandler 
from crewai.tools.course_planner_tool import course_planner_tool
from crewai.tasks.course_planner_tasks import generate_course_plan_task
from agents.course_planner_agent import course_planner_agent

# Initialize memory handler for the agent
memory_handler = MemoryHandler(
    session_id="course_planner_session",                    
    file_path="memory/course_planner_memory.json"
)   

# Tool for course planner agent
course_tool = course_planner_tool()


course_planner_agent = Agent(
    name="CoursePlannerAgent",
    role="Curriculum progression planner for educators",
    goal=(
        "Analyze student performance and recommend the next best topic aligned with curriculum progression, "
        "difficulty level, and quiz mastery. Help teachers plan their instruction more effectively."
    ),
    backstory="""
CoursePlannerAgent is designed to support teachers in planning what to teach next. 
It analyzes quiz outcomes, topic dependencies, and overall mastery to recommend the next topic. 
It reduces the burden of manual planning and adapts to class-level performance. 
The agent ensures logical topic flow and pacing, suitable for grades 1–10 and UG.
It uses inputs from QuizAgent, StudentLevelAgent, and TeacherDashboardAgent to form decisions.
It is optimized for use in rural classrooms, ensuring no child is left behind.
It provides both a standard and an adaptive recommendation with reasoning.
It respects grade-level learning objectives and links to prior topics.
It can also optionally recommend related research papers or stories.
It outputs a clear JSON for integration into dashboards or printed sheets.
""",
    memory=True,
    memory_handler=memory_handler,
    allow_delegation=True,
    verbose=True,
    tools=[course_tool],
    tasks=[generate_course_plan_task],
    user_type="teacher",
    metadata={
        "grade_range": "1-10 and UG",
        "subject_areas": "All subjects",
        "language_support": "Regional dialects supported"
    },
    session_memory_handler=memory_handler,
    session_tools=[course_tool],
    session_tasks=[generate_course_plan_task],
    llm_config={"model": "gemini-pro", "temperature": 0.6},
    respect_context_window=True,
    code_execution_config={"enabled": True,
    "executor_type": "kirchhoff-async"
    },
)
course_planner_agent.add_input("QuizAgent")
course_planner_agent.add_input("StudentLevelAgent")
course_planner_agent.add_input("TeacherDashboardAgent")
course_planner_agent.add_output("NextTopicRecommendation")
course_planner_agent.add_output("AdaptiveNextTopicRecommendation")
course_planner_agent.add_output("RelatedResearchPapers")
course_planner_agent.add_output("RelatedStories")
course_planner_agent.add_output("JSONOutput")
course_planner_agent.add_output("TeacherInstructionPlan")
course_planner_agent.add_output("ClassLevelPerformanceSummary")
course_planner_agent.add_output("CurriculumProgressionReport")
course_planner_agent.add_output("PacingGuide")
course_planner_agent.add_output("LogicalTopicFlow")
)

# Optional advanced inputs:
course_planner_agent.add_input("ContentCreatorAgent")
course_planner_agent.add_input("PredictiveAnalyticsAgent")
