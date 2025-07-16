from crewflows import Agent
from crewflows.memory import MemoryHandler
from tasks.student_level_analytics_task import generate_student_analytics_task
from tools.student_level_analytics_tool import student_level_analytics_tool

# Initialize memory handler for this agent session
memory_handler = MemoryHandler(
    session_id="student_analytics_session",
    file_path="memory/student_analytics_memory.json"
)

# Define the Student Level Analytics Agent
student_level_analytics_agent = Agent(
    name="StudentLevelAnalyticsAgent",
    role="Per-student learning performance evaluator",
    goal=(
        "Analyze individual student's quiz history to find gaps in understanding, track progress over time, "
        "and provide personalized feedback. Recommend targeted concepts for revision and future learning."
    ),
    backstory=(
        "This agent helps teachers and students understand individual learning patterns, "
        "track strengths and weaknesses, and receive actionable study advice. "
        "It works in offline-first mode and syncs analytics through SyncAgent."
    ),
    memory=True,
    memory_handler=memory_handler,
    allow_delegation=False,
    verbose=True,
    tools=[student_level_analytics_tool],
    tasks=[generate_student_analytics_task],
    user_type="teacher",
    metadata={
        "analysis_type": "student",
        "output_format": "JSON"
    },
    llm_config={"model": "gemini-pro", "temperature": 0.5},
    respect_context_window=True,
    code_execution_config={"enabled": True, "executor_type": "kirchhoff-async"},
)

# Define inputs accepted by the agent
student_level_analytics_agent.add_input("student_performance")

# Define outputs produced by the agent
student_level_analytics_agent.add_output("strengths")
student_level_analytics_agent.add_output("weaknesses")
student_level_analytics_agent.add_output("recommendations")
student_level_analytics_agent.add_output("progress_score")
