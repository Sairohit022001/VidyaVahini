from crewflows import Agent  # temporarily commented out

from crewflows.memory import MemoryHandler
from crewai.tasks import content_creation_task
from crewflows.tools.content_creation_tool import content_creation_tool 
      

memory_handler = MemoryHandler(
    session_id="content_creator_agent_session",
    file_path="memory/content_creator_agent_memory.json"
)   

content_creation_tool = content_creation_tool()

content_creator_agent = Agent(
    name="ContentCreatorAgent",
    role="Multimodal content assembly assistant for teachers",
    goal="""
1. Allow teachers to combine AI content with their notes.
2. Import lesson/story/quiz components into one view.
3. Enable drag-and-drop editing for lesson structure.
4. Accept teacher-uploaded PDFs or DOCs for mixing with AI.
5. Validate final output for structure and readability.
6. Output content in class-friendly formats (HTML, PDF).
7. Recommend visuals, quiz links, and story embeds.
8. Provide translation into local dialects if needed.
9. Save drafts and allow publishing to class portal.
10. Improve AI-human co-creation without code.
""",
    backstory="""
1. Created for teacher-led final lesson assembly.
2. Supports multimodal integration: story + quiz + visuals.
3. Connects to VisualAgent and LessonPlannerAgent outputs.
4. Used for final review before sharing with students.
5. Allows manual edits, annotations, and summary notes.
6. Teachers can override AI-generated text.
7. Allows real-time preview of composed lesson.
8. Exports in offline-compatible formats.
9. Works offline with sync queue to push drafts.
10. Helps teachers bridge between AI assistance and human experience.
""",
    memory=True,
    memory_handler=memory_handler,
    allow_delegation=True,
    verbose=True,
    tools=[content_creation_tool],
    tasks=[content_creation_task],
    user_type="teacher",
    metadata={
        "grade_range": "1-10 and UG",
        "subject_areas": "All subjects",
        "language_support": "Regional dialects supported"   
    },
    session_memory_handler=memory_handler,
    session_tools=[content_creation_tool],
    session_tasks=[content_creation_task],
    llm_config={"model": "gemini-pro", "temperature": 0.6},
    respect_context_window=True,
    code_execution_config={
        "enabled": True,
        "executor_type": "kirchhoff-async"
    },
)

content_creator_agent.add_input("StoryTellerAgent")
content_creator_agent.add_input("QuizAgent")
content_creator_agent.add_input("LessonPlannerAgent")

content_creator_agent.add_output("LessonDraft")
content_creator_agent.add_output("CombinedLessonModule")
content_creator_agent.add_output("PublishedLesson")
content_creator_agent.add_output("TeacherNotes")