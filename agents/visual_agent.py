from crewflows import Agent
from tools.visual_generation_tool import VisualGenerationTool
from tasks.visual_generation_task import VisualGenerationTask
from crewflows.memory.local_memory_handler import LocalMemoryHandler
from langchain_google_genai import ChatGoogleGenerativeAI
import os
# Initialize the visual generation tool instance
visual_generation_tool = VisualGenerationTool()

# Memory handler for visual agent
memory_handler = LocalMemoryHandler(
    session_id="visual_agent_session",
    file_path="memory/visual_agent_memory.json"
)

class VisualAgent(Agent):
    def __init__(self):
        super().__init__(
            name="VisualAgent",
            role=(
                """1. Generate visually engaging illustrations for educational concepts.
2. Adapt visuals based on student grade level and age group.
3. Ensure all images reflect the cultural and regional context.
4. Convert lesson summaries and storylines into scene-level prompts.
5. Support teachers in explaining complex topics through visual storytelling.
6. Create visual aids like diagrams, cartoons, and symbolic illustrations.
7. Enable prompt-based image generation using DALL·E or Gemini Vision.
8. Align generated visuals with dialect, tone, and local curriculum.
9. Seamlessly integrate with StoryTellerAgent and LessonPlannerAgent.
10. Output AI-generated images or prompts ready for PDF export or display."""
            ),
            goal=(
                "Given lesson plans or story text, generate culturally relevant and grade-appropriate visuals "
                "including scene prompts and images. Adapt output for dialect, curriculum, and learner age."
            ),
            backstory=(
                """1. VisualAgent was built to enhance concept delivery through vivid imagery.
2. It serves Indian classrooms where abstract concepts often need visual aids.
3. Designed with rural and multilingual students in mind to reduce learning gaps.
4. It converts lesson summaries or stories into meaningful visual prompts.
5. Automatically adapts illustration tone based on grade and dialect.
6. Supports culturally relevant depictions to ensure relatability.
7. Bridges text-heavy material with visuals for better understanding.
8. Works alongside StoryTellerAgent and LessonPlannerAgent.
9. Produces scenes, diagrams, or charts tailored to the academic level.
10. Makes education more inclusive, interactive, and retention-friendly."""
            ),
            tools=[visual_generation_tool],
            memory=True,
            memory_handler=memory_handler,
            allow_delegation=True,
            verbose=True,
            llm_config={
                "model": "models/gemini-2.5-pro",
                "temperature": 0.7,
                "max_tokens": 2048
            },
            respect_context_window=True,
            code_execution_config={
                "enabled": True,
                "executor_type": "kirchhoff-async"
            },
            user_type="teacher",
            metadata={
                "grade_range": "1-10 and UG",
                "access": "teacher_only",
                "delegates_to": ["StoryTellerAgent", "LessonPlannerAgent"]
            },
            tasks=[] # Remove the task from the tasks list in super().__init__
        )
        # Store the task instance in a dedicated instance variable
        self.visual_generation_task_instance = VisualGenerationTask(name=VisualGenerationTask.name, description=VisualGenerationTask.description)

    async def process(self, inputs: dict):
        """
        Asynchronously processes input to generate visuals.
        
        Args:
            inputs (dict): Includes lesson_plan_json, story_text, dialect, etc.
        
        Returns:
            dict: Dictionary with dalle_prompts, generated_images, scene_descriptions or error.
        """
        try:
            context = {
                "lesson_plan_json": inputs.get("lesson_plan_json"),
                "story_text": inputs.get("story_text"),
                "dialect": inputs.get("dialect", "default")
            }

            # Access the task instance from the instance variable and run it
            result = await self.visual_generation_task_instance.run(context)
            return result

        except Exception as e:
            return {"error": f"[VisualAgent] process() failed: {str(e)}"}

# Instantiate and wire the agent
visual_agent = VisualAgent()

# Input Sources
visual_agent.add_input("LessonPlannerAgent")
visual_agent.add_input("StoryTellerAgent")

# Output Types
visual_agent.add_output("dalle_prompts")
visual_agent.add_output("generated_images")
visual_agent.add_output("scene_descriptions")
