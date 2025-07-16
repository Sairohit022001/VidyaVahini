from crewflows import Agent
from agents.lesson_planner_agent import lesson_planner_agent
from tools.lesson_generation_tool import LessonGenerationTool
from tasks.lesson_planner_tasks import generate_lesson_task
from crewflows.memory.local_memory_handler import LocalMemoryHandler 
    

#This memory handler will store the session data for the lesson planner agent 
memory_handler = LocalMemoryHandler(
    session_id="teacher_lesson_session",
    file_path="memory/lesson_planner_memory.json"
)

#Tool for lesson planner agent
lesson_tool = LessonGenerationTool()

#Define Agent
lesson_planner_agent = Agent(
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

# Explicitly declare accepted input sources
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