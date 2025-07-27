import os
import json
import types
import logging
from crewflows import Agent
from tools.quiz_generation_tool import QuizGenerationTool
from tasks.quiz_tasks import QuizTask
from crewflows.memory.local_memory_handler import LocalMemoryHandler
from langchain_google_genai import ChatGoogleGenerativeAI

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# =====================================================
# ✅ Initialize Memory
# =====================================================
memory_handler = LocalMemoryHandler(
    session_id="quiz_agent_session",
    file_path="memory/quiz_agent_memory.json"
)

# =====================================================
# ✅ Initialize Tool
# =====================================================
quiz_tool = QuizGenerationTool()

# =====================================================
# ✅ Helper: Fallback
# =====================================================
def get_quiz_fallback():
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

def validate_quiz_output(model_output):
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


# =====================================================
# ✅ QuizAgent Class
# =====================================================
class QuizAgent(Agent):
    def __init__(self, *args, **kwargs):
        # Filter invalid tasks
        if 'tasks' in kwargs and isinstance(kwargs['tasks'], list):
            kwargs['tasks'] = [
                t for t in kwargs['tasks']
                if not (hasattr(t, '__class__') and t.__class__.__name__ == 'Task')
            ]

        super().__init__(*args, **kwargs)

        self.quiz_task_instance = QuizTask(
            name=QuizTask.name,
            description=QuizTask.description
        )

    async def process(self, inputs: dict):
        """Main async process method."""
        lesson_plan = inputs.get("lesson_plan_json")
        story = inputs.get("story_body")
        audio_data = inputs.get("audio_data")
        dialect = inputs.get("dialect", "default")

        if not any([lesson_plan, story, audio_data]):
            return {"error": "QuizAgent requires lesson_plan_json, story_body, or audio_data."}

        context = {
            "lesson_plan_json": lesson_plan,
            "story_body": story,
            "audio_data": audio_data,
            "dialect": dialect
        }

        try:
            # ✅ Try primary QuizTask
            quiz_task_result = await self.quiz_task_instance.run(context)

            # ✅ Handle explicit error dicts
            if isinstance(quiz_task_result, dict) and ("error" in quiz_task_result or "error_details" in quiz_task_result):
                logger.warning(f"QuizTask returned error: {quiz_task_result}")
                return quiz_tool.get_quiz_fallback()

            # ✅ Validate & Return
            return validate_quiz_output(quiz_task_result)

        except Exception as e:
            logger.exception("QuizAgent process() failed")
            return get_quiz_fallback()


# =====================================================
# ✅ Instantiate Agent
# =====================================================
quiz_agent = QuizAgent(
    name="QuizAgent",
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

# =====================================================
# ✅ Add Inputs & Outputs
# =====================================================
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

# =====================================================
# ✅ Sync Wrapper
# =====================================================
def sync_process(self, inputs: dict):
    import asyncio
    result = asyncio.run(self.process(inputs))
    return validate_quiz_output(result)

quiz_agent.sync_process = types.MethodType(sync_process, quiz_agent)
