import os
import json
import types
import logging
from typing import Any, Dict, Optional

from crewflows import Agent
from crewflows.memory.local_memory_handler import LocalMemoryHandler
from langchain_google_genai import ChatGoogleGenerativeAI

from tools.quiz_generation_tool import QuizGenerationTool
from tasks.quiz_tasks import QuizTask

# ✅ Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# ✅ Initialize memory handler
memory_handler = LocalMemoryHandler(
    session_id="quiz_agent_session",
    file_path="memory/quiz_agent_memory.json"
)

# ✅ Tool instance
quiz_tool = QuizGenerationTool()


class QuizAgent(Agent):
    quiz_task_instance: QuizTask
    _name: str

    def __init__(self, *args: Any, name: Optional[str] = None, **kwargs: Any) -> None:
        if 'tasks' in kwargs and isinstance(kwargs['tasks'], list):
            kwargs['tasks'] = [
                t for t in kwargs['tasks']
                if not (hasattr(t, '__class__') and t.__class__.__name__ == 'Task')
            ]

        super().__init__(*args, name=name or "quiz_agent", **kwargs)
        self._name = name or "quiz_agent"
        self.quiz_task_instance = QuizTask(
            name=QuizTask.name,
            description=QuizTask.description
        )

    @property
    def name(self) -> str:
        return self._name

    async def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        lesson_plan = inputs.get("lesson_plan_json")
        story = inputs.get("story_body")
        audio_data = inputs.get("audio_data")
        dialect = inputs.get("dialect", "default")

        logger.info(f"QuizAgent.process called with dialect: {dialect}")
        if lesson_plan:
            logger.info(f"Lesson plan keys: {list(lesson_plan.keys())}")
        if story:
            logger.info(f"Story body preview: {story[:100]}")
        if audio_data:
            logger.info(f"Audio data received (length: {len(audio_data)})")

        if not any([lesson_plan, story, audio_data]):
            logger.error("QuizAgent.process requires at least one of lesson_plan_json, story_body, or audio_data.")
            return {"error": "QuizAgent requires lesson_plan_json, story_body, or audio_data."}

        context = {
            "lesson_plan_json": lesson_plan,
            "story_body": story,
            "audio_data": audio_data,
            "dialect": dialect
        }

        try:
            quiz_task_result = await self.quiz_task_instance.run(context)
            if isinstance(quiz_task_result, dict) and ("error" in quiz_task_result or "error_details" in quiz_task_result):
                logger.warning(f"QuizTask returned error: {quiz_task_result}")
                return get_quiz_fallback()
            return validate_quiz_output(quiz_task_result)
        except Exception:
            logger.exception("QuizAgent process() failed, returning fallback quiz.")
            return get_quiz_fallback()


def get_quiz_fallback() -> Dict[str, Any]:
    """Fallback quiz when model output is invalid."""
    return {
        "quiz_json": {
            "questions": [
                {
                    "question_text": "What is photosynthesis?",
                    "options": [
                        "Process of making food by plants",
                        "Breathing process",
                        "Water cycle",
                        "Seed germination"
                    ],
                    "correct_answer": "Process of making food by plants",
                    "explanation": "Photosynthesis is how plants make food."
                }
            ],
            "format_type": "MCQ",
            "topic": "Photosynthesis",
            "grade_level": "7",
            "total_marks": 1,
            "dialect_adapted": False
        },
        "adaptive_quiz_set": {"easy": [], "medium": [], "hard": []},
        "retry_feedback_report": {}
    }


def validate_quiz_output(model_output: Any) -> Dict[str, Any]:
    """Ensure the quiz output is valid and contains required keys."""
    try:
        data = json.loads(model_output) if isinstance(model_output, str) else model_output
        if not isinstance(data, dict):
            logger.warning("Model output is not a dict. Using fallback.")
            return get_quiz_fallback()

        required_keys = ["quiz_json", "adaptive_quiz_set", "retry_feedback_report"]
        if not all(k in data for k in required_keys):
            logger.warning("Model output missing keys. Using fallback.")
            return get_quiz_fallback()

        return data
    except json.JSONDecodeError:
        logger.error("Invalid JSON. Using fallback.")
        return get_quiz_fallback()


# ✅ Instantiate QuizAgent
quiz_agent = QuizAgent(
    name="quiz_agent",
    role="AI-based adaptive quiz generator",
    goal="Generate quizzes from lessons, stories, and audio data with adaptive difficulty.",
    backstory="QuizAgent helps teachers by generating quizzes automatically and adapting to student performance.",
    memory=True,
    memory_handler=memory_handler,
    allow_delegation=True,
    verbose=True,
    tools=[quiz_tool],
    tasks=[],
    llm=ChatGoogleGenerativeAI(
        model="models/gemini-2.5-pro",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.3
    ),
    respect_context_window=True,
    code_execution_config={"enabled": True, "executor_type": "kirchhoff-async"},
    user_type="teacher",
    metadata={
        "grade_range": "1-10 and UG",
        "access": "teacher_and_student",
        "downstream": ["CoursePlannerAgent", "GamificationAgent"],
        "triggers": ["on_lesson_completion"]
    }
)

# ✅ Register input and output fields
quiz_agent.add_input("lesson_plan_json")
quiz_agent.add_input("story_body")
quiz_agent.add_input("audio_data")
quiz_agent.add_input("dialect")
quiz_agent.add_input("LessonPlannerAgent")
quiz_agent.add_input("StoryTellerAgent")
quiz_agent.add_input("VoiceTutorAgent")

quiz_agent.add_output("quiz_json")
quiz_agent.add_output("adaptive_quiz_set")
quiz_agent.add_output("retry_feedback_report")

# ✅ CLI-compatible sync wrapper
def sync_process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
    import asyncio
    result = asyncio.run(self.process(inputs))
    return validate_quiz_output(result)

quiz_agent.sync_process = types.MethodType(sync_process, quiz_agent)
