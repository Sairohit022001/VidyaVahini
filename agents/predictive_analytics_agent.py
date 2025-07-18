from crewflows import Agent
from crewflows.memory.local_memory_handler import LocalMemoryHandler 
from tools.predictive_analytics_tool import predictive_analytics_tool
from tasks.predictive_analytics_task import generate_class_analytics_task 

memory_handler = LocalMemoryHandler(
    session_id="predictive_analytics_session",
    file_path="memory/predictive_analytics_memory.json"
)

class PredictiveAnalyticsAgent(Agent):
    def __init__(self):
        super().__init__(
            name="PredictiveAnalyticsAgent",
            role="""
1. Analyze class-wide quiz data for actionable insights.
2. Identify top-performing students and struggling learners.
3. Detect common weak concepts across the class.
4. Track learning trends and engagement patterns over time.
5. Provide recommendations for lesson revisions and pacing.
6. Generate structured JSON reports for dashboards.
7. Integrate seamlessly with TeacherDashboardAgent.
8. Support offline sync and data caching via SyncAgent.
9. Help teachers make data-driven instructional decisions.
10. Enhance overall classroom learning effectiveness.
""",
            goal="""
Given aggregated quiz data, generate actionable class-level analytics and detailed reports for teachers to improve instructional outcomes.
""",
            backstory="""
1. Built to reduce teacher workload on performance analysis.
2. Aggregates individual quiz results for holistic class view.
3. Highlights trends not visible at single-student level.
4. Assists in planning focused group interventions.
5. Works closely with dashboard and content planning agents.
6. Designed for resource-constrained rural and urban classrooms.
7. Supports low-connectivity environments through caching.
8. Provides transparent, interpretable reports for teachers.
9. Encourages proactive teaching adjustments.
10. Empowers teachers with timely data insights for better outcomes.
""",
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

    async def process(self, inputs: dict):
        """
        Process aggregated quiz data asynchronously to generate class-level analytics.

        Args:
            inputs (dict): Inputs from QuizAgent or other relevant data sources.

        Returns:
            dict: Structured JSON report with class performance insights.
        """
        try:
            result = await generate_class_analytics_task.run(inputs)
            return result
        except Exception as e:
            return {"error": f"PredictiveAnalyticsAgent process() failed: {str(e)}"}

predictive_analytics_agent = PredictiveAnalyticsAgent()

# Declare accepted inputs
predictive_analytics_agent.add_input("QuizAgent")
