import logging
import os
import asyncio
import types
from crewflows import Agent
from typing import Any, Dict
from tools.lesson_generation_tool import LessonGenerationTool
from tasks.lesson_planner_tasks import generate_lesson_task
from crewflows.memory.local_memory_handler import LocalMemoryHandler
from langchain_google_genai import ChatGoogleGenerativeAI

# Load API key from env
google_api_key = os.getenv("GOOGLE_API_KEY")

# Memory handler
memory_handler = LocalMemoryHandler(
    session_id="teacher_lesson_session",
    file_path="memory/lesson_planner_memory.json"
)

# LLM config
llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-pro",
    google_api_key=google_api_key,
    temperature=0.3
)

# Tool for lesson generation
lesson_tool = LessonGenerationTool()

class LessonPlannerAgent(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def process(self, inputs: dict):
        topic = inputs.get("topic")
        level = inputs.get("level") or "Medium"
        dialect = inputs.get("dialect", "default")
        context_from_doc = inputs.get("context_from_doc", {})

        if not topic:
            return {"error": "Missing required input 'topic'"}

        context = {
            "topic": topic,
            "level": level,
            "dialect": dialect,
            "context_from_doc": context_from_doc,
        }

        try:
            result = await asyncio.to_thread(lesson_tool.run, context)
            logging.info(f"LessonTool result: {result}")

            if not result:
                return {"error": "LessonGenerationTool returned empty result"}

            if not isinstance(result, dict):
                return {"error": f"Invalid result type: {type(result)}"}

            return result

        except Exception as e:
            logging.error(f"LessonPlannerAgent process() failed: {e}", exc_info=True)
            return {"error": f"LessonPlannerAgent process() failed: {str(e)}"}


# Instantiate agent
lesson_planner_agent = LessonPlannerAgent(
    name="lesson_planner_agent",
    role="AI co-teacher that helps educators design structured lessons, quizzes, stories, and visual content.",
    goal="""...""",  
    backstory="""...""",  
    memory=True,
    memory_handler=memory_handler,
    allow_delegation=True,
    verbose=True,
    tools=[lesson_tool],
    tasks=[generate_lesson_task],
    llm=llm,
    respect_context_window=True,
    code_execution_config={
        "enabled": True,
        "executor_type": "kirchhoff-async"
    },
    user_type="teacher",
    metadata={ ... }  # unchanged
)

# Inputs
lesson_planner_agent.add_input("topic")
lesson_planner_agent.add_input("level")
lesson_planner_agent.add_input("dialect")
lesson_planner_agent.add_input("context_from_doc")
lesson_planner_agent.add_input("MultimodalResearchAgent")

# Outputs
lesson_planner_agent.add_output("lesson_plan_json")
lesson_planner_agent.add_output("core_concepts_list")
lesson_planner_agent.add_output("lesson_summary")
lesson_planner_agent.add_output("suggested_agents")
lesson_planner_agent.add_output("recommended_visuals")
lesson_planner_agent.add_output("linked_story_prompts")
lesson_planner_agent.add_output("quiz_questions")
lesson_planner_agent.add_output("regional_language_support")
lesson_planner_agent.add_output("offline_exportable_content")

# Optional: Sync wrapper for Swagger/cURL
def sync_process(self, inputs: dict):
    return asyncio.run(self.process(inputs))

lesson_planner_agent.sync_process = types.MethodType(sync_process, lesson_planner_agent)