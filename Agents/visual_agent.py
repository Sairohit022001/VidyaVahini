from crewai import Agent
from tools.visual_generation_tool import VisualGenerationTool
from tasks.visual_agent_tasks import generate_visuals_task
from memory.memory_handler import MemoryHandler 

# Initialize the visual generation tool
visual_generation_tool = VisualGenerationTool() 

# Set up memory handler for the visual agent
memory_handler = MemoryHandler(
    session_id="visual_agent_session",      
    file_path="memory/visual_agent_memory.json"
)   

# Define the VisualAgent with its properties and capabilities

visual_agent = Agent(
    name="VisualAgent",
    role="AI assistant for educational illustration generation",
    goal=(
    "1. Generate visually engaging illustrations for educational concepts.\n"
    "2. Adapt visuals based on student grade level and age group.\n"
    "3. Ensure all images reflect the cultural and regional context.\n"
    "4. Convert lesson summaries and storylines into scene-level prompts.\n"
    "5. Support teachers in explaining complex topics through visual storytelling.\n"
    "6. Create visual aids like diagrams, cartoons, and symbolic illustrations.\n"
    "7. Enable prompt-based image generation using DALL·E or Gemini Vision.\n"
    "8. Align generated visuals with dialect, tone, and local curriculum.\n"
    "9. Seamlessly integrate with StoryTellerAgent and LessonPlannerAgent.\n"
    "10. Output AI-generated images or prompts ready for PDF export or display."
)
    backstory=(
    "1. VisualAgent was built to enhance concept delivery through vivid imagery.\n"
    "2. It serves Indian classrooms where abstract concepts often need visual aids.\n"
    "3. Designed with rural and multilingual students in mind to reduce learning gaps.\n"
    "4. It converts lesson summaries or stories into meaningful visual prompts.\n"
    "5. Automatically adapts illustration tone based on grade and dialect.\n"
    "6. Supports culturally relevant depictions to ensure relatability.\n"
    "7. Bridges text-heavy material with visuals for better understanding.\n"
    "8. Works alongside StoryTellerAgent and LessonPlannerAgent.\n"
    "9. Produces scenes, diagrams, or charts tailored to the academic level.\n"
    "10. Makes education more inclusive, interactive, and retention-friendly."
)
    tools=["dalle", "gemini_vision"],
    tool_descriptions={
        "dalle": "Generate images based on text prompts using DALL·E.",
        "gemini_vision": "Create visual content using Gemini Vision based on provided descriptions."
    },
    tool_use_policy="use tools when necessary",
    tool_use_policy_description=(
        "VisualAgent uses tools like DALL·E or Gemini Vision to generate images "
        "when it needs to create visual content based on text prompts or scene descriptions. "
        "It will utilize these tools to produce illustrations that align with educational goals, "
        "cultural context, and student needs. The agent will only use these tools when it
        "deems it necessary to fulfill its role in generating educational visuals."
    ),
    memory=True,
    memory_handler=MemoryHandler(
        session_id="visual_agent_session",
        file_path="memory/visual_agent_memory.json"
    ),
    allow_delegation=True,
    verbose=True,       
    llm_config={"model": "gemini-pro", "temperature": 0.7, "max_tokens": 2048},
    respect_context_window=True,
    code_execution_config={"enabled": False},       
    user_type="teacher",        
    metadata={
        "grade_range": "1-10 and UG",
        "access": "teacher_only",
        "delegates_to": ["StoryTellerAgent", "LessonPlannerAgent"]
    }       
)


visual_agent.add_input("LessonPlannerAgent")
visual_agent.add_input("StoryTellerAgent")
visual_agent.add_output("dalle_prompts")
visual_agent.add_output("generated_images")
visual_agent.add_output("scene_descriptions")