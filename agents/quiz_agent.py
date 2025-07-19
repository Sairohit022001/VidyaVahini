from crewflows import Agent
from tools.quiz_generation_tool import QuizGenerationTool
from crewflows.memory.local_memory_handler import LocalMemoryHandler
from tasks.quiz_tasks import QuizTask # Import the class
# Assuming Task is crewai.Task, you might need to import it if used for type checking
# from crewai import Task
from langchain_google_genai import ChatGoogleGenerativeAI
import os
# Initialize memory handler for QuizAgent
memory_handler = LocalMemoryHandler(
    session_id="quiz_agent_session",
    file_path="memory/quiz_agent_memory.json"
)

# Initialize the quiz generation tool
quiz_tool = QuizGenerationTool()

class QuizAgent(Agent):
    def __init__(self, *args, **kwargs):
        # Remove the task from the tasks list in super().__init__
        if 'tasks' in kwargs and isinstance(kwargs['tasks'], list):
            # Assuming Task is crewai.Task, adjust condition if needed
            kwargs['tasks'] = [task for task in kwargs['tasks'] if not (hasattr(task, '__class__') and task.__class__.__name__ == 'Task')]
        super().__init__(*args, **kwargs)

        # Store the task instance in a dedicated instance variable
        self.quiz_task_instance = QuizTask(name=QuizTask.name, description=QuizTask.description)


    async def process(self, inputs: dict):
        # Extract inputs from upstream agents
        lesson_plan = inputs.get("lesson_plan_json")
        story = inputs.get("story_body")
        audio_data = inputs.get("audio_data")  # from VoiceTutorAgent or BhāṣāGuru
        dialect = inputs.get("dialect", "default")

        # Validate inputs (at least one content source needed)
        if not any([lesson_plan, story, audio_data]):
            return {"error": "QuizAgent requires at least one input: lesson_plan_json, story_body, or audio_data"}

        context = {
            "lesson_plan_json": lesson_plan,
            "story_body": story,
            "audio_data": audio_data,
            "dialect": dialect,
            # Add other relevant keys as needed
        }

        try:
            # Access the task instance from the instance variable and run it
            result = await self.quiz_task_instance.run(context)
            return result
        except Exception as e:
            return {"error": f"QuizAgent process() failed: {str(e)}"}

# Instantiate your agent
quiz_agent = QuizAgent(
    name="QuizAgent",
    role="AI-based adaptive quiz generator",
    goal="""
1. Automatically generate adaptive quizzes based on AI-generated lessons, stories, and student proficiency levels.
2. Create various question formats: MCQs, fill-in-the-blanks, true/false, short answers.
3. Ensure age-appropriate difficulty aligned with grade and topic complexity.
4. Incorporate regional context and dialect for cultural relevance.
5. Provide explanations and formative feedback per question.
6. Integrate with LessonPlannerAgent, StoryTellerAgent, and VoiceTutorAgent.
7. Enable retry mode for mastery by regenerating questions on incorrect answers.
8. Support offline-first delivery with caching and Firestore sync via SyncAgent.
9. Assist teachers in monitoring engagement, scores, and misconceptions.
10. Output structured JSON for export, audio narration, or classroom use.
""",
    backstory="""
QuizAgent is an AI assistant creating dynamic, culturally aware quizzes aligned with India's classrooms. 
It bridges AI content and assessments, supporting retries and explanation-based learning.
Works with LessonPlannerAgent, StoryTellerAgent, BhāṣāGuru for voice-enabled assessments.
Tracks progress for teacher dashboards.
""",
    memory=True,
    memory_handler=memory_handler,
    allow_delegation=True,
    verbose=True,
    tools=[quiz_tool],
    tasks=[], # Removed the task from the tasks list
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

# Declare accepted inputs
quiz_agent.add_input("lesson_plan_json")
quiz_agent.add_input("story_body")
quiz_agent.add_input("audio_data")
quiz_agent.add_input("dialect")
quiz_agent.add_input("LessonPlannerAgent")
quiz_agent.add_input("StoryTellerAgent")  # for story-based quizzes
quiz_agent.add_input("VoiceTutorAgent")   # for audio narration of quizzes
quiz_agent.add_input("BhāṣāGuru")         # for dialect-specific audio

# Declare expected outputs
quiz_agent.add_output("quiz_json")
quiz_agent.add_output("adaptive_quiz_set")
quiz_agent.add_output("student_scores")
quiz_agent.add_output("retry_feedback_report")

import types
def sync_process(self, inputs: dict):
    import asyncio
    return asyncio.run(self.process(inputs))

quiz_agent.sync_process = types.MethodType(sync_process, quiz_agent)
