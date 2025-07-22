from crewflows import Agent
from crewflows.memory.local_memory_handler import LocalMemoryHandler
from tasks.ask_me_task import ask_question_task
from tools.ask_me_tool import AskMeTool
from langchain_google_genai import ChatGoogleGenerativeAI
import os
# Memory handler setup for session persistence
memory_handler = LocalMemoryHandler(
    session_id="ask_me_agent_session",
    file_path="memory/ask_me_agent_memory.json"
)

# Tool setup
askme_tool = AskMeTool()

class AskMeAgent(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def process(self, inputs: dict):
        try:
            # You can adapt input keys as needed here
            question = inputs.get("user_question")
            dialect = inputs.get("user_dialect")
            grade = inputs.get("user_grade")
            lesson_content = inputs.get("current_lesson_content")
            past_lessons = inputs.get("past_lessons", {})
            research_pdfs = inputs.get("research_pdfs", {})
            session_memory = inputs.get("session_memory", {})

            context = {
                "question": question,
                "dialect": dialect,
                "grade": grade,
                "current_lesson_content": lesson_content,
                "past_lessons": past_lessons,
                "research_pdfs": research_pdfs,
                "session_memory": session_memory,
            }

            result = await ask_question_task.run(context)
            return result
        except Exception as e:
            return {"error": f"AskMeAgent process() failed: {str(e)}"}

# Instantiate the agent
ask_me_agent = AskMeAgent(
    name="AskMeAgent",
    role="Contextual Q&A assistant for teachers and advanced learners",
    goal=(
        "1. Accurately answer academic questions using contextual memory.\n"
        "2. Adapt explanations to the user's level, dialect, and current lesson.\n"
        "3. Ground responses in structured lesson data, summaries, and research.\n"
        "4. Collaborate with BhāṣāGuru for voice output when requested.\n"
        "5. Enable follow-up planning through CoursePlannerAgent.\n"
        "6. Maintain live session memory across Q&A interactions."
    ),
    backstory=(
        "AskMeAgent serves as the trusted knowledge assistant within VidyaVāhinī. "
        "It uses real-time memory, lesson context, and regional understanding to deliver accurate, helpful, and grounded answers. "
        "Its goal is to support teachers and students alike with in-depth explanations, summaries, and follow-up suggestions—while ensuring low hallucination."
    ),
    memory=True,
    memory_handler=memory_handler,
    allow_delegation=True,
    verbose=True,
    tools=[askme_tool],
    tasks=[ask_question_task],
    user_type="teacher",
    metadata={
        "supported_grades": "1-12, UG",
        "supported_subjects": "All core subjects",
        "dialect_adaptation": True,
        "voice_narration": True,
        "integration_ready": ["BhāṣāGuru", "CoursePlannerAgent"]
    },
    llm=ChatGoogleGenerativeAI(
        model="models/gemini-2.5-pro",
        google_api_key= os.getenv("GEMINI_API_KEY"),
        temperature=0.3
    ),
    respect_context_window=True,
    code_execution_config={
        "enabled": True,
        "executor_type": "kirchhoff-async"
    },
)

# Agent input sources
ask_me_agent.add_input([
    "LessonPlannerAgent",
    "QuizAgent",
    "TeacherDashboardAgent",
    "CoursePlannerAgent",
    "BhāṣāGuru",
    "user_question",
    "user_dialect",
    "user_grade",
    "current_lesson_content",
    "past_lessons",
    "research_pdfs",
    "classroom_summaries",
    "session_memory"
])

# Agent output fields
ask_me_agent.add_output([
    "contextual_answer",
    "source_explanation",
    "followup_prompt",
    "audio_narration"
])
