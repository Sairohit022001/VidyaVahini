import os
import types
from crewflows import Agent
from tools.quiz_generation_tool import QuizGenerationTool
from tasks.quiz_tasks import QuizTask
from crewflows.memory.local_memory_handler import LocalMemoryHandler
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize memory
memory_handler = LocalMemoryHandler(
    session_id="quiz_agent_session",
    file_path="memory/quiz_agent_memory.json"
)

# Initialize tool
quiz_tool = QuizGenerationTool()

class QuizAgent(Agent):
    def __init__(self, *args, **kwargs):
        # Remove default Task objects from crewai if mistakenly passed
        if 'tasks' in kwargs and isinstance(kwargs['tasks'], list):
            kwargs['tasks'] = [task for task in kwargs['tasks'] if not (hasattr(task, '__class__') and task.__class__.__name__ == 'Task')]
        super().__init__(*args, **kwargs)

        # Manually instantiate task
        self.quiz_task_instance = QuizTask(
            name=QuizTask.name,
            description=QuizTask.description
        )

    async def process(self, inputs: dict):
        lesson_plan = inputs.get("lesson_plan_json")
        story = inputs.get("story_body")
        audio_data = inputs.get("audio_data")
        dialect = inputs.get("dialect", "default")

        # Validate required inputs
        if not any([lesson_plan, story, audio_data]):
            return {
                "error": "QuizAgent requires at least one input: lesson_plan_json, story_body, or audio_data"
            }

        context = {
            "lesson_plan_json": lesson_plan,
            "story_body": story,
            "audio_data": audio_data,
            "dialect": dialect,
        }

        try:
            result = await self.quiz_task_instance.run(context)

            # Validate result structure
            if not isinstance(result, dict):
                return {"error": f"Expected dict from QuizTask.run(), got {type(result)}"}

            expected_keys = ["quiz_json", "adaptive_quiz_set"]
            missing_keys = [k for k in expected_keys if k not in result]
            if missing_keys:
                return {"error": f"Missing keys in quiz result: {missing_keys}"}

            return result

        except Exception as e:
            return {"error": f"QuizAgent process() failed: {str(e)}"}


# Instantiate agent
quiz_agent = QuizAgent(
    name="QuizAgent",
    role="AI-based adaptive quiz generator",
    goal="""...""",  # goal truncated for brevity
    backstory="""...""",
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

# Inputs accepted from upstream agents
quiz_agent.add_input("lesson_plan_json")
quiz_agent.add_input("story_body")
quiz_agent.add_input("audio_data")
quiz_agent.add_input("dialect")
quiz_agent.add_input("LessonPlannerAgent")
quiz_agent.add_input("StoryTellerAgent")
quiz_agent.add_input("VoiceTutorAgent")
quiz_agent.add_input("BhāṣāGuru")

# Expected outputs
quiz_agent.add_output("quiz_json")
quiz_agent.add_output("adaptive_quiz_set")
quiz_agent.add_output("student_scores")
quiz_agent.add_output("retry_feedback_report")

# Sync wrapper
def sync_process(self, inputs: dict):
    import asyncio
    return asyncio.run(self.process(inputs))

quiz_agent.sync_process = types.MethodType(sync_process, quiz_agent)
