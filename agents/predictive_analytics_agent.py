from crewflows import Agent
from crewflows.memory import MemoryHandler
from crewflows.tools.predictive_analytics_tool import predictive_analytics_tool
from crewflows.tasks.predictive_analytics_task import generate_class_analytics_task


memory_handler = MemoryHandler(
    session_id="predictive_analytics_session",
    file_path="memory/predictive_analytics_memory.json"
)

predictive_analytics_agent = Agent(
    name="PredictiveAnalyticsAgent",
    role="Class-level analytics generator for quiz results",
    goal=(
        "Analyze aggregated quiz results from QuizAgent to provide class-level insights such as average score, "
        "top-performing students, class-wide weak concepts, and learning trends. "
        "Support teachers in planning future lessons based on whole-class performance patterns. "
        "Generate structured JSON reports for integration with teacher dashboards and decision making."
    ),
    backstory=(
        "This agent supports teachers by analyzing class-wide quiz data to identify group-level performance patterns. "
        "It surfaces trends, recommends topics for revision, and assists in class-level planning. "
        "Designed to integrate with TeacherDashboardAgent and support offline caching with SyncAgent."
    ),
    memory=True,
    memory_handler=memory_handler,
    allow_delegation=False,
    verbose=True,
    tools=[predictive_analytics_tool],
    tasks=[generate_class_analytics_task],
    user_type="teacher",
    metadata={
        "analysis_type": "class_level",
        "output_format": "JSON"
    },
    llm_config={"model": "gemini-pro", "temperature": 0.5},
    respect_context_window=True,
    code_execution_config={"enabled": True, "executor_type": "kirchhoff-async"},
)

predictive_analytics_agent.add_input("QuizAgent")
