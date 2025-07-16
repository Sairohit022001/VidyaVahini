from crewflows import Agent
from crewflows.memory.local_memory_handler import LocalMemoryHandler
from tools.student_level_analytics_tool import student_level_analytics_tool

# Initialize memory handler for Student Level Analytics Agent
memory_handler = LocalMemoryHandler(
    session_id="student_analytics_session",
    file_path="memory/student_analytics_memory.json"
)

student_level_analytics_agent = Agent(
    name="StudentLevelAnalyticsAgent",
    role="Per-student learning performance evaluator",
    goal=(
        "Analyze individual student's quiz history to identify gaps, "
        "track progress over time, and provide personalized feedback."
    ),
    backstory=(
        "Assists teachers and students in understanding learning patterns, strengths, weaknesses, "
        "and delivers tailored study advice."
    ),
    memory=True,
    memory_handler=memory_handler,
    allow_delegation=False,
    verbose=True,
    tools=[student_level_analytics_tool],  # Tool instance assigned here
    tasks=[],  # Initially empty, task assigned dynamically below
    user_type="teacher",
    metadata={
        "analysis_type": "student",
        "output_format": "JSON"
    },
    llm_config={"model": "gemini-pro", "temperature": 0.5},
    respect_context_window=True,
    code_execution_config={"enabled": True, "executor_type": "kirchhoff-async"},
)

# Import task here to avoid circular imports
from tasks.student_level_analytics_task import generate_student_analytics_task

# Dynamically assign the agent and tool to the task
generate_student_analytics_task.agent = student_level_analytics_agent
generate_student_analytics_task.tool = student_level_analytics_tool
