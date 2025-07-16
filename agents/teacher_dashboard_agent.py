from crewflows import Agent
from crewflows.memory.local_memory_handler import LocalMemoryHandler
from tools.dashboard_tool import TeacherDashboardTool
from tasks.dashboard_tasks import generate_dashboard_metrics_task

# Initialize dashboard tool
teacher_dashboard_tool = TeacherDashboardTool()

# Initialize memory handler
memory_handler = LocalMemoryHandler(
    session_id="teacher_dashboard_agent_session",
    file_path="memory/teacher_dashboard_agent_memory.json"
)

teacher_dashboard_agent = Agent(
    name="TeacherDashboardAgent",
    role="Real-time analytics and alert generator for teachers",
    goal="""
1. Aggregate all student activity and quiz data in real time.
2. Generate weekly teaching metrics and summaries.
3. Raise alerts for at-risk or inactive students.
4. Visualize per-topic and per-student performance.
5. Help teachers adjust pacing and difficulty based on insights.
6. Flag dropout risks or significant performance drops.
7. Provide a single-glance view of class health.
8. Integrate predictive insights to support decisions.
9. Track engagement trends over weeks.
10. Enable data-driven teaching with auto-refinement suggestions.
""",
    backstory="""
1. Designed to reduce teachers' manual tracking burden.
2. Pulls data from all learning agents and analytics tools.
3. Offers timeline-based performance summaries.
4. Makes abstract metrics simple and actionable.
5. Works closely with PredictiveAnalyticsAgent.
6. Central dashboard for decision-making and class review.
7. Offers alerts, progress graphs, and usage analytics.
8. Accessible to teachers via web dashboard and mobile app.
9. Informs CoursePlannerAgent for adaptive flows.
10. Anchored in making teachers' work smarter and not harder.
""",
    tools=[teacher_dashboard_tool],
    tasks=[generate_dashboard_metrics_task],
    memory=True,
    memory_handler=memory_handler,
    allow_delegation=True,
    verbose=True,
    llm_config={"model": "gemini-pro", "temperature": 0.7, "max_tokens": 2048},
    respect_context_window=True,
    code_execution_config={"enabled": True, "executor_type": "kirchhoff-async"},
    user_type="teacher",
    metadata={
        "grade_range": "1-10 and UG",
        "access": "teacher_only",
        "delegates_to": ["PredictiveAnalyticsAgent"]
    }
)

# Declare accepted inputs
teacher_dashboard_agent.add_input("QuizAgent")
teacher_dashboard_agent.add_input("StudentLevelAgent")
teacher_dashboard_agent.add_input("PredictiveAnalyticsAgent")

# Declare expected outputs
teacher_dashboard_agent.add_output("WeeklyMetrics")
teacher_dashboard_agent.add_output("DropoutAlerts")
teacher_dashboard_agent.add_output("LessonViewStats")
teacher_dashboard_agent.add_output("StruggleFlags")
teacher_dashboard_agent.add_output("EngagementReport")
