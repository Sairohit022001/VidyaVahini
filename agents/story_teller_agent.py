import os
import types
from crewflows import Agent
from tools.story_generation_tool import StoryGenerationTool
from tasks.story_teller_tasks import StoryTellerTask
from crewflows.memory.local_memory_handler import LocalMemoryHandler
from langchain_google_genai import ChatGoogleGenerativeAI

# Memory handler
memory_handler = LocalMemoryHandler(
    session_id="story_teller_agent_session",
    file_path="memory/story_teller_agent_memory.json"
)

# Tool
story_tool = StoryGenerationTool()

class StoryTellerAgent(Agent):
    def __init__(self, *args, **kwargs):
        # Remove default task if accidentally passed
        if 'tasks' in kwargs and isinstance(kwargs['tasks'], list):
            kwargs['tasks'] = [task for task in kwargs['tasks'] if not (hasattr(task, '__class__') and task.__class__.__name__ == 'Task')]
        super().__init__(*args, **kwargs)

        # Inject task manually
        self.story_teller_task_instance = StoryTellerTask(
            name=StoryTellerTask.name,
            description=StoryTellerTask.description
        )

    async def process(self, inputs: dict):
        lesson_plan = inputs.get("lesson_plan_json")
        topic = inputs.get("topic")
        level = inputs.get("level")
        dialect = inputs.get("dialect", "default")

        if not lesson_plan:
            return {"error": "Missing required input 'lesson_plan_json'"}
        if not topic:
            return {"error": "Missing required input 'topic'"}

        context = {
            "lesson_plan_json": lesson_plan,
            "topic": topic,
            "level": level,
            "dialect": dialect,
        }

        try:
            result = await self.story_teller_task_instance.run(context)

            # Validate result structure
            if not isinstance(result, dict):
                return {"error": f"Expected dict but got {type(result)}"}

            # Check for expected keys
            expected_keys = ["story_title", "story_body", "moral"]
            missing_keys = [k for k in expected_keys if k not in result]
            if missing_keys:
                return {"error": f"Missing keys in result: {missing_keys}"}

            return result

        except Exception as e:
            return {"error": f"StoryTellerAgent process() failed: {str(e)}"}


# Instantiate
story_teller_agent = StoryTellerAgent(
    id="story-teller-agent",
    name="StoryTellerAgent",
    role="AI assistant for generating contextual, cultural stories for teachers",
    goal="""...""",  # Truncated
    backstory="""...""",  # Truncated
    tools=[story_tool],
    tasks=[],  # removed task from init
    memory=True,
    memory_handler=memory_handler,
    allow_delegation=True,
    verbose=True,
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
        "access": "teacher_only",
        "delegates_to": ["VisualAgent"]
    }
)

# Inputs
story_teller_agent.add_input("lesson_plan_json")
story_teller_agent.add_input("topic")
story_teller_agent.add_input("level")
story_teller_agent.add_input("dialect")

# Outputs
story_teller_agent.add_output("story_title")
story_teller_agent.add_output("story_body")
story_teller_agent.add_output("moral")
story_teller_agent.add_output("visual_prompts")
story_teller_agent.add_output("localized_dialect_story")
story_teller_agent.add_output("audio_narration")

# Sync wrapper for Swagger/cURL
def sync_process(self, inputs: dict):
    import asyncio
    return asyncio.run(self.process(inputs))

story_teller_agent.sync_process = types.MethodType(sync_process, story_teller_agent)
