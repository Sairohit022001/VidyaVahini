from crewflows import Agent
from crewflows.memory.local_memory_handler import LocalMemoryHandler
from tasks.content_creation_tasks import generate_content_task
from tools.content_creation_tool import ContentCreationTool
from langchain_google_genai import ChatGoogleGenerativeAI
import os
# Initialize memory handler
memory_handler = LocalMemoryHandler(
    session_id="content_creator_agent_session",
    file_path="memory/content_creator_agent_memory.json"
)

# Instantiate the content creation tool
content_creation_tool = ContentCreationTool()

class ContentCreatorAgent(Agent):
    def __init__(self):
        super().__init__(
            name="ContentCreatorAgent",
            role="""
                    1. Assist teachers in assembling multimodal educational content efficiently.
                    2. Combine AI-generated lessons, stories, quizzes with teacher notes.
                    3. Provide drag-and-drop UI integration for lesson structure editing.
                    4. Accept and integrate uploaded teacher documents (PDF, DOC).
                    5. Validate final content for pedagogical structure and clarity.
                    6. Output class-friendly formats: HTML, PDF, offline compatible.
                    7. Suggest visuals, quiz references, and story embeds contextually.
                    8. Support translations into regional dialects.
                    9. Enable draft saving and publishing workflows.
                    10. Facilitate seamless AI-human collaborative lesson creation.
                    """,
            goal="""
                    Help teachers assemble, validate, and publish high-quality multimodal educational content by integrating AI-generated modules and human input.
                """,
            backstory="""
                    1. Designed to empower teachers as final content curators.
                    2. Bridges AI content generation with human intuition and edits.
                    3. Integrates outputs from StoryTellerAgent, QuizAgent, LessonPlannerAgent.
                    4. Allows manual overrides, annotations, and summary notes.
                    5. Supports real-time preview of assembled lessons.
                    6. Exports lessons suitable for offline use and easy distribution.
                    7. Works with offline sync to queue drafts when no connectivity.
                    8. Enables teachers to build lessons without needing coding skills.
                    9. Serves rural and multilingual education contexts.
                    10. Enhances teacher autonomy while leveraging AI assistance.
                    """,
            memory=True,
            memory_handler=memory_handler,
            allow_delegation=True,
            verbose=True,
            tools=[content_creation_tool],
            tasks=[generate_content_task],
            user_type="teacher",
            metadata={
                "grade_range": "1-10 and UG",
                "subject_areas": "All subjects",
                "language_support": "Regional dialects supported"
            },
            llm=ChatGoogleGenerativeAI(
            model="models/gemini-2.5-pro",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.3
            ),
            respect_context_window=True,
            code_execution_config={
                "enabled": True,
                "executor_type": "kirchhoff-async"
            },
        )

    async def process(self, inputs: dict):
        """
        Process inputs asynchronously to assemble multimodal content.

        Args:
            inputs (dict): Expected keys include StoryTellerAgent, QuizAgent, LessonPlannerAgent content.

        Returns:
            dict: Combined lesson draft, notes, and publishable modules.
        """
        try:
            # Run content generation task
            result = await generate_content_task.run(inputs)
            return result
        except Exception as e:
            return {"error": f"ContentCreatorAgent process() failed: {str(e)}"}

content_creator_agent = ContentCreatorAgent()

# Declare inputs from other agents
content_creator_agent.add_input("StoryTellerAgent")
content_creator_agent.add_input("QuizAgent")
content_creator_agent.add_input("LessonPlannerAgent")

# Declare outputs expected from this agent
content_creator_agent.add_output("LessonDraft")
content_creator_agent.add_output("CombinedLessonModule")
content_creator_agent.add_output("PublishedLesson")
content_creator_agent.add_output("TeacherNotes")
