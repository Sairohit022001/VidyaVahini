from crewflows import Agent
from crewflows.memory.local_memory_handler import LocalMemoryHandler 
from tools.course_planner_tool import CoursePlannerTool  
from tasks.course_planner_tasks import generate_course_plan_task
import types
import inspect
import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Initialize memory handler for the agent
memory_handler = LocalMemoryHandler(
    session_id="course_planner_session",                    
    file_path="memory/course_planner_memory.json"
)   

# Tools for course planner agent
course_tool = CoursePlannerTool()

course_planner_agent = Agent(
    name="CoursePlannerAgent",
    role="Curriculum progression planner for educators",
    goal=(
        "Analyze student performance and recommend the next best topic aligned with curriculum progression, "
        "difficulty level, and quiz mastery. Help teachers plan their instruction more effectively. "
        "It can either use uploaded PDF content or stored database lessons, and can optionally include predictive analytics results if the teacher manually chooses."
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
    llm=ChatGoogleGenerativeAI(
        model="models/gemini-2.5-pro",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.3
    ),
    respect_context_window=True,
    code_execution_config={
        "enabled": True,
        "executor_type": "kirchhoff-async"
    },
)


course_planner_agent.add_input("PredictiveAnalyticsAgent")
course_planner_agent.add_input("PDFFile")
course_planner_agent.add_input("DatabaseLesson")
course_planner_agent.add_input("UsePredictiveAnalyticsFlag")

# Register outputs
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
course_planner_agent.add_output("CoursePlanTimeline")  # ✅ New
course_planner_agent.add_output("AnalyticsUsed")       # ✅ New

# Updated async process method
async def process(self, input_data):
    """
    Runs all assigned tasks sequentially or as per framework logic,
    passing input_data and returning aggregated result.
    """

    use_analytics = input_data.get("use_predictive_analytics", False)
    pdf_path = input_data.get("pdf_path")
    db_lesson_id = input_data.get("db_lesson_id")

    # 1. Extract lesson content (PDF or DB)
    if pdf_path:
        lesson_text = await pdf_tool.extract_text(pdf_path)
    elif db_lesson_id:
        lesson_text = course_tool.fetch_from_db(db_lesson_id)
    else:
        raise ValueError("No PDF or Database lesson provided.")

    # 2. Optionally fetch analytics
    analytics_data = None
    if use_analytics:
        analytics_data = self.get_input("PredictiveAnalyticsAgent")

    # 3. Generate course plan
    task_data = {
        "lesson_text": lesson_text,
        "analytics_data": analytics_data,
        "use_analytics": use_analytics
    }

    results = {}
    for task in getattr(self, "tasks", []):
        if hasattr(task, "run") and callable(task.run):
            if inspect.iscoroutinefunction(task.run):
                result = await task.run(task_data)
            else:
                result = task.run(task_data)
            results[task.__class__.__name__] = result
        elif callable(task):
            if inspect.iscoroutinefunction(task):
                result = await task(task_data)
            else:
                result = task(task_data)
            results[task.__class__.__name__] = result
        else:
            raise AttributeError(f"Task {task} has no runnable method.")
    return results

# Bind updated async process method
course_planner_agent.process = types.MethodType(process, course_planner_agent)
