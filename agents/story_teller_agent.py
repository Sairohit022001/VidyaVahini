from crewflows import Agent
from tools.story_generation_tool import StoryGenerationTool
from tasks.story_teller_tasks import StoryTellerTask # Import the class
from crewflows.memory.local_memory_handler import LocalMemoryHandler
# Assuming Task is crewai.Task, you might need to import it if used for type checking
# from crewai import Task
from langchain_google_genai import ChatGoogleGenerativeAI
import os
# Memory handler for story teller agent
memory_handler = LocalMemoryHandler(
    session_id="story_teller_agent_session",
    file_path="memory/story_teller_agent_memory.json"
)

# Tool for story teller agent
story_tool = StoryGenerationTool()

class StoryTellerAgent(Agent):
    def __init__(self, *args, **kwargs):
        # Remove the task from the tasks list in super().__init__
        if 'tasks' in kwargs and isinstance(kwargs['tasks'], list):
            # Assuming Task is crewai.Task, adjust condition if needed
            kwargs['tasks'] = [task for task in kwargs['tasks'] if not (hasattr(task, '__class__') and task.__class__.__name__ == 'Task')]
        super().__init__(*args, **kwargs)

        # Store the task instance in a dedicated instance variable
        self.story_teller_task_instance = StoryTellerTask(name=StoryTellerTask.name, description=StoryTellerTask.description)


    async def process(self, inputs: dict):
        lesson_plan = inputs.get("lesson_plan_json")
        topic = inputs.get("topic")
        level = inputs.get("level")
        dialect = inputs.get("dialect", "default")

        # Input validation to avoid empty calls
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
            # Access the task instance from the instance variable and run it
            result = await self.story_teller_task_instance.run(context)
            return result
        except Exception as e:
            return {"error": f"StoryTellerAgent process() failed: {str(e)}"}

# Instantiate your agent
story_teller_agent = StoryTellerAgent(
    id="story-teller-agent",
    name="StoryTellerAgent",
    role="""AI assistant for generating contextual, cultural stories for teachers""",
    goal="""
1. Convert educational topics into engaging, age-appropriate narratives.
2. Ensure storytelling is culturally contextualized and dialect-sensitive.
3. Include regionally grounded characters, locations, and scenarios.
4. Embed morals and values suitable for classroom discussion.
5. Output structured JSON compatible with UI story cards.
6. Recommend visual prompts for VisualAgent or DALL·E.
7. Collaborate seamlessly with BhāṣāGuru for audio narration.
8. Dynamically adjust tone and vocabulary based on grade (Class 1-10 or UG).
9. Generate multilingual-ready stories with flexible prompt formatting.
10. Empower teachers to make lessons interactive through storytelling.
""",
    backstory="""
1. StoryTellerAgent is a narrative co-teacher built for culturally adaptive classrooms across India.
2. It supports multilingual and regional storytelling tailored to grade-level understanding.
3. Designed for teachers in rural, government, and low-connectivity schools to simplify abstract ideas.
4. Helps make topics emotionally engaging through familiar characters, settings, and tones.
5. Aligns stories with grade curriculum while embedding regional morals or real-life examples.
6. Works closely with VisualAgent to generate scene-level illustrations from suggested prompts.
7. Generates dialect-specific content, making the learning environment inclusive and relatable.
8. Supports BhāṣāGuru for SSML-based storytelling in audio using native dialects.
9. Ensures every story embeds a purpose: moral learning, curiosity, or conceptual clarity.
10. Its ultimate goal is to empower teachers with engaging narrative tools, not replace them.
""",
    tools=[story_tool],
    tasks=[], # Removed the task from the tasks list
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

# Declare inputs and outputs
story_teller_agent.add_input("lesson_plan_json")
story_teller_agent.add_input("topic")
story_teller_agent.add_input("level")
story_teller_agent.add_input("dialect")

story_teller_agent.add_output("story_title")
story_teller_agent.add_output("story_body")
story_teller_agent.add_output("moral")
story_teller_agent.add_output("visual_prompts")
story_teller_agent.add_output("localized_dialect_story")
story_teller_agent.add_output("audio_narration")

import types
def sync_process(self, inputs: dict):
    import asyncio
    return asyncio.run(self.process(inputs))

story_teller_agent.sync_process = types.MethodType(sync_process, story_teller_agent)
