from crewai import Agent

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
    verbose=True
    allow_delegation=True,
    memory=True,
    context_strategy="reflexion",
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
