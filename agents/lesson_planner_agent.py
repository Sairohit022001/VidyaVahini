from crewflows import Agent
from tools.lesson_generation_tool import LessonGenerationTool
from tasks.lesson_planner_tasks import generate_lesson_task
from crewflows.memory.local_memory_handler import LocalMemoryHandler
from langchain_google_genai import ChatGoogleGenerativeAI
import os
# Load API key from environment
google_api_key = os.getenv("GOOGLE_API_KEY")

# Memory handler for the lesson planner agent
memory_handler = LocalMemoryHandler(
    session_id="teacher_lesson_session",
    file_path="memory/lesson_planner_memory.json"
)

# Define the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro-latest",
    google_api_key=google_api_key,
    temperature=0.3
)

# Tool for lesson planner agent
lesson_tool = LessonGenerationTool()

class LessonPlannerAgent(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def process(self, inputs: dict):
        topic = inputs.get("topic")
        level = inputs.get("level")
        dialect = inputs.get("dialect")
        context_from_doc = inputs.get("context_from_doc", {})

        context = {
            "topic": topic,
            "level": level,
            "dialect": dialect,
            "context_from_doc": context_from_doc,
        }

        # Run the lesson generation tool
        result = lesson_tool.run(inputs=context)
        return result

# Instantiate the agent
lesson_planner_agent = LessonPlannerAgent(
    name="lesson_planner_agent",
    role="AI co-teacher that helps educators design structured lessons, quizzes, stories, and visual content.",
    goal="""
Support teachers in generating clear, curriculum-aligned lesson content.
Produce structured lessons tailored to students' grade level and cognitive ability.
Enable regional language support using dialect-specific translations.
Collaborate with story, quiz, and visual generation agents to enrich delivery.
Assist teachers in adapting lessons for Class 1-10 and undergraduate learners.
Generate optional branches for deeper exploration using research agents.
Create explainable outputs that can be exported or taught offline.
Empower low-resource educators to deliver AI-enhanced, multimodal lessons.
Maintain alignment with state curriculum frameworks and teaching outcomes.
Trigger follow-up agents such as CoursePlanner and BhāṣāGuru post-lesson.
""",
    backstory="""
You are VidyaVāhinī's core lesson generation agent, designed to assist teachers across India.
You work like a co-teacher—deeply aware of classroom dynamics, student comprehension, and teacher intent.
You specialize in generating explainable, localized, and adaptive lesson content.
You collaborate with VisualAgent, StoryTellerAgent, QuizAgent, and MultimodalResearchAgent.
You delegate tasks like quiz generation or image creation when needed.
Teachers trust you to generate reliable lesson flows, even in offline-first environments.
You can adjust tone, complexity, and dialect for regional classrooms.
You are not meant to be used by students directly, but empower teachers to guide them.
You remember prior lesson context to avoid redundancy and support continuity.
Your mission is to uplift classrooms by turning teacher ideas into structured educational experiences.
""",
    memory=True,
    memory_handler=memory_handler,
    allow_delegation=True,
    verbose=True,
    tools=[lesson_tool],
    tasks=[generate_lesson_task],
    llm_config={"model": "gemini-pro", "temperature": 0.6},
    respect_context_window=True,
    code_execution_config={
        "enabled": True,
        "executor_type": "kirchhoff-async"
    },
    user_type="teacher",
    metadata={
        "grade_range": "1-10 and UG",
        "access": "teacher_only",
        "delegates_to": [
            "QuizAgent",
            "StoryTellerAgent",
            "VisualAgent",
            "MultimodalResearchAgent"
        ],
        "accepts_context_from": [
            "MultimodalResearchAgent",
            "UploadedPDFs",
            "StudentLevelAgent",
            "CoursePlannerAgent"
        ],
        "outputs": [
            "lesson_plan_json",
            "core_concepts_list",
            "lesson_summary",
            "suggested_agents",
            "recommended_visuals",
            "linked_story_prompts",
            "quiz_questions",
            "regional_language_support",
            "offline_exportable_content"
        ]
    }
)

# Declare accepted inputs
lesson_planner_agent.add_input("topic")
lesson_planner_agent.add_input("level")
lesson_planner_agent.add_input("dialect")
lesson_planner_agent.add_input("context_from_doc")
lesson_planner_agent.add_input("MultimodalResearchAgent")

# Declare expected outputs
lesson_planner_agent.add_output("lesson_plan_json")
lesson_planner_agent.add_output("core_concepts_list")
lesson_planner_agent.add_output("lesson_summary")
lesson_planner_agent.add_output("suggested_agents")
lesson_planner_agent.add_output("recommended_visuals")
lesson_planner_agent.add_output("linked_story_prompts")
lesson_planner_agent.add_output("quiz_questions")
lesson_planner_agent.add_output("regional_language_support")
lesson_planner_agent.add_output("offline_exportable_content")







from crewai import Agent
from tools.lesson_generation_tool import lesson_tool
from langchain_google_genai import ChatGoogleGenerativeAI
from tasks.lesson_planner_task import LessonPlannerTask
import os
from typing import Any, Dict

# Load API key from environment
google_api_key = os.getenv("GOOGLE_API_KEY")

# Define the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro-latest",
    google_api_key=google_api_key,
    temperature=0.3
)

# Define the Lesson Planner Agent
lesson_planner_agent = Agent(
    name="LessonPlannerAgent",
    role="Curriculum and Lesson Designer",
    goal=(
        "Design engaging and research-backed lessons for students based on selected topic, level, and region."
    ),
    backstory=(
        "You are an expert lesson planner specializing in regional curriculum design. "
        "You break down complex topics into understandable lessons, drawing from relevant research, "
        "ensuring students of all levels can learn effectively."
    ),
    verbose=True,
    allow_delegation=False,
    tools=[lesson_tool],
    llm=llm
)

# Wrapper class to use in main.py or orchestrator
class LessonPlannerAgentWrapper:
    def __init__(self):
        self.agent = lesson_planner_agent
        self.task = LessonPlannerTask()

    async def execute(self, topic: str, level: str, dialect: str = "default", context_from_doc: Dict = {}) -> Dict[str, Any]:
        """
        Execute the Lesson Planner agent asynchronously.

        Args:
            topic (str): The educational topic to generate a lesson on.
            level (str): The difficulty level (e.g., primary, secondary).
            dialect (str): The regional dialect to use.
            context_from_doc (dict): Optional context from uploaded PDF.

        Returns:
            dict: Structured lesson plan including concept explanation, research, questions, etc.
        """
        return await self.task.run(topic, level, dialect, context_from_doc)

    async def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Alternative interface using dictionary-based inputs (for crew integration).

        Args:
            inputs (dict): Dictionary with 'topic', 'level', 'dialect', and optional 'context_from_doc'.

        Returns:
            dict: Lesson output or error.
        """
        topic = inputs.get("topic")
        level = inputs.get("level")
        dialect = inputs.get("dialect", "default")
        context_from_doc = inputs.get("context_from_doc", {})

        context = {
            "topic": topic,
            "level": level,
            "dialect": dialect,
            "context_from_doc": context_from_doc
        }

        try:
            result = lesson_tool.run(inputs=context)

            if isinstance(result, dict):
                return result
            elif isinstance(result, list):
                return result[0] if result else {}
            else:
                return {"lesson_output": str(result).strip()}

        except Exception as e:
            return {"error": f"LessonPlannerAgent process() failed: {str(e)}"}
