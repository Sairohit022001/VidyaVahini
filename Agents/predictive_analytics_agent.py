from crewai import Agent
from crewai.memory import MemoryHandler
from crewai.tools.predictive_analytics_tool import predictive_analytics_tool
from crewai.tasks.predictive_analytics_task import generate_class_analytics_task

memory_handler = MemoryHandler(
    session_id="predictive_analytics_session",
    file_path="memory/predictive_analytics_memory.json"
)

predictive_analytics_agent = Agent(
    name="PredictiveAnalyticsAgent",
    role="Class-level analytics generator for quiz results",
    goal=(
        "Analyze quiz results from QuizAgent and provide class-level analytics, "
        "including average score, top performers, areas of weakness for each student, and recommendations."
        "create actionable insights for teachers to improve student learning outcomes."
        "Assist in planning future lessons based on class performance trends."
        "Generate structured reports that can be integrated into teacher dashboards."
        "Support offline-first delivery where analytics are cached and sync back with Firestore via SyncAgent."
        "Help teachers monitor class engagement, scores, misconceptions, and student-specific patterns."
        
    ),
    backstory=(
        "This agent helps teachers understand class performance on quizzes, "
        "identifies trends, and suggests interventions for improvement"
        "It generates structured reports that can be used in teacher dashboards or printed sheets."
        "It is designed to work seamlessly with QuizAgent and TeacherDashboardAgent, "
    ),
    memory=True,
    memory_handler=memory_handler,
    allow_delegation=False,
    verbose=True,
    tools=[predictive_analytics_tool],
    tasks=[generate_class_analytics_task],
    user_type="teacher",
    metadata={
        "analysis_type": "quiz",
        "output_format": "JSON"
    },
    llm_config={"model": "gemini-pro", "temperature": 0.5},
    respect_context_window=True,
    code_execution_config={"enabled": False},
)
predictive_analytics_agent.add_input("QuizAgent")