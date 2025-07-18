from crewflows import Agent
from crewflows.memory.local_memory_handler import LocalMemoryHandler
from tools.student_level_analytics_tool import student_level_analytics_tool

# Initialize memory handler for Student Level Analytics Agent
memory_handler = LocalMemoryHandler(
    session_id="student_analytics_session",
    file_path="memory/student_analytics_memory.json"
)

class StudentLevelAnalyticsAgent(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def process(self, inputs: dict):
        try:
            # Extract relevant input data for analysis
            quiz_history = inputs.get("quiz_history", {})
            student_id = inputs.get("student_id")
            timeframe = inputs.get("timeframe", "last_month")
            additional_context = inputs.get("additional_context", {})

            context = {
                "quiz_history": quiz_history,
                "student_id": student_id,
                "timeframe": timeframe,
                "additional_context": additional_context
            }

            # Run the analysis task asynchronously
            from tasks.student_level_analytics_task import generate_student_analytics_task
            result = await generate_student_analytics_task.run(context)

            return result
        except Exception as e:
            return {"error": f"StudentLevelAnalyticsAgent process() failed: {str(e)}"}

student_level_analytics_agent = StudentLevelAnalyticsAgent(
    name="StudentLevelAnalyticsAgent",
    role="""Per-student learning performance evaluator focused on individualized insights and recommendations:
1. Analyze quiz attempts and accuracy trends per student.
2. Identify learning gaps and misconceptions.
3. Track progress over different timeframes.
4. Provide personalized feedback and study recommendations.
5. Detect topic mastery and retention issues.
6. Support teachers with actionable insights for interventions.
7. Integrate with other agents for holistic learner profiles.
8. Adapt to student learning pace and style.
9. Maintain privacy and session-based memory securely.
10. Export findings in JSON for dashboards and reports.
""",
    goal="""To empower educators by delivering in-depth, personalized student learning analytics,
highlighting strengths, weaknesses, and progress trajectories to inform targeted teaching strategies.""",
    backstory="""StudentLevelAnalyticsAgent acts as the dedicated analytics partner,
helping teachers and students make sense of individual learning journeys.
It synthesizes quiz data, performance metrics, and contextual info into clear insights,
supporting continuous improvement and personalized learning experiences.
It complements other VidyaVāhinī agents by providing foundational data-driven feedback.""",
    memory=True,
    memory_handler=memory_handler,
    allow_delegation=False,
    verbose=True,
    tools=[student_level_analytics_tool],  # Tool instance assigned here
    tasks=[],  # Task assigned dynamically below
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
