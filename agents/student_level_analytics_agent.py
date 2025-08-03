from crewflows import Agent
from crewflows.memory.local_memory_handler import LocalMemoryHandler
from tools.student_level_analytics_tool import student_level_analytics_tool
from tasks.student_level_analytics_task import StudentLevelAnalyticsTask
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from typing import Any, Dict, Optional

load_dotenv()

# Use consistent key for Google API — adjust if both keys are required
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not GOOGLE_API_KEY:
    raise EnvironmentError("Required Google API key (GOOGLE_API_KEY or GEMINI_API_KEY) not set")


# Initialize memory handler
memory_handler = LocalMemoryHandler(
    session_id="student_analytics_session",
    file_path="memory/student_analytics_memory.json"
)


# Instantiate the global task once
student_analytics_task = StudentLevelAnalyticsTask()


class StudentLevelAnalyticsAgent(Agent):
    def __init__(self, *args, name: str = "student_level_analytics_agent", **kwargs):
        super().__init__(*args, name=name, **kwargs)
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    async def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        try:
            quiz_history = inputs.get("quiz_history", {})
            student_id = inputs.get("student_id")
            timeframe = inputs.get("timeframe", "last_month")
            additional_context = inputs.get("additional_context", {})

            context = {
                "quiz_history": quiz_history,
                "student_id": student_id,
                "timeframe": timeframe,
                "additional_context": additional_context,
            }

            result = await student_analytics_task.run(context)
            return result

        except Exception as e:
            return {"error": f"StudentLevelAnalyticsAgent process() failed: {str(e)}"}


# Instantiate the agent
student_level_analytics_agent = StudentLevelAnalyticsAgent(
    name="student_level_analytics_agent",
    role=(
        "Per-student learning performance evaluator focused on individualized insights and recommendations:\n"
        "1. Analyze quiz attempts and accuracy trends per student.\n"
        "2. Identify learning gaps and misconceptions.\n"
        "3. Track progress over different timeframes.\n"
        "4. Provide personalized feedback and study recommendations.\n"
        "5. Detect topic mastery and retention issues.\n"
        "6. Support teachers with actionable insights for interventions.\n"
        "7. Integrate with other agents for holistic learner profiles.\n"
        "8. Adapt to student learning pace and style.\n"
        "9. Maintain privacy and session-based memory securely.\n"
        "10. Export findings in JSON for dashboards and reports."
    ),
    goal=(
        "To empower educators by delivering in-depth, personalized student learning analytics, "
        "highlighting strengths, weaknesses, and progress trajectories to inform targeted teaching strategies."
    ),
    backstory=(
        "StudentLevelAnalyticsAgent acts as the dedicated analytics partner, "
        "helping teachers and students make sense of individual learning journeys. "
        "It synthesizes quiz data, performance metrics, and contextual info into clear insights, "
        "supporting continuous improvement and personalized learning experiences. "
        "It complements other VidyaVāhinī agents by providing foundational data-driven feedback."
    ),
    memory=True,
    memory_handler=memory_handler,
    allow_delegation=False,
    verbose=True,
    tools=[student_level_analytics_tool],
    tasks=[student_analytics_task],
    user_type="teacher",
    metadata={
        "analysis_type": "student",
        "output_format": "JSON"
    },
    llm=ChatGoogleGenerativeAI(
        model="models/gemini-2.5-pro",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.3
    ),
    respect_context_window=True,
    code_execution_config={"enabled": True, "executor_type": "kirchhoff-async"},
)

# Bind task references for integration
student_analytics_task.agent = student_level_analytics_agent
student_analytics_task.tool = student_level_analytics_tool
