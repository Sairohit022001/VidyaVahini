from crewflows import Agent
from crewflows.memory.local_memory_handler import LocalMemoryHandler
from tasks.ask_me_task import ask_question_task
from tools.ask_me_tool import AskMeTool

memory_handler = LocalMemoryHandler(
    session_id="ask_me_agent_session",
    file_path="memory/ask_me_agent_memory.json"
)

askme_tool = AskMeTool()

ask_me_agent = Agent(
    name="AskMeAgent",
    role="Contextual Q&A support for teachers, Intermediate and Undergraduate students",
    goal="""
1. Resolve academic doubts using large language models with contextual memory.
2. Interpret user questions in the context of current and past lessons.
3. Serve teachers across grades with deep explanations and follow-up resources.
4. Assist students of Grade 11 and above with self-guided conceptual learning.
5. Adapt answers to user's dialect and preferred complexity level.
6. Inject classroom content, summaries, and research into the response.
7. Prevent AI hallucination by grounding outputs in structured lesson data.
8. Provide audio narration of answers via BhāṣāGuru when requested.
9. Enable future recommendations via CoursePlannerAgent interlinking.
10. Maintain session memory for ongoing Q&A threads in a live class environment.
""",
    backstory="""
AskMeAgent is the intelligent backbone of VidyaVāhinī's contextual doubt-solving system.
It is designed to support both teachers and advanced learners by delivering high-quality, grounded answers.
In real-time classroom scenarios, it references past lessons, dialectal nuances, and research PDFs to ensure reliable output.
Its integration with memory and crew context allows it to mimic the intuition of an experienced educator.
AskMeAgent respects the learning stage of the user: simplifying for beginners, elaborating for advanced students,
and helping teachers reinforce or extend explanations. It's a bridge between classroom discussion and personalized inquiry.
It can also collaborate with BhāṣāGuru for voice narration or CoursePlannerAgent for guiding follow-ups.
""",
    memory=True,
    memory_handler=memory_handler,
    allow_delegation=True,
    verbose=True,
    tools=[askme_tool],
    tasks=[ask_question_task],
    user_type="teacher",
    metadata={
        "grade_range": "1-10 and UG",
        "subject_areas": "All subjects",
        "language_support": "Regional dialects supported"
    },
    llm_config={"model": "gemini-pro", "temperature": 0.6},
    respect_context_window=True,
    code_execution_config={
        "enabled": True,
        "executor_type": "kirchhoff-async"
    },
)

# Inputs
ask_me_agent.add_input("LessonPlannerAgent")
ask_me_agent.add_input("QuizAgent")
ask_me_agent.add_input("TeacherDashboardAgent")
ask_me_agent.add_input("CoursePlannerAgent")
ask_me_agent.add_input("BhāṣāGuru")
ask_me_agent.add_input("user_question")
ask_me_agent.add_input("user_dialect")
ask_me_agent.add_input("user_grade")
ask_me_agent.add_input("current_lesson_content")
ask_me_agent.add_input("past_lessons")
ask_me_agent.add_input("research_pdfs")
ask_me_agent.add_input("classroom_summaries")
ask_me_agent.add_input("session_memory")

# Outputs
ask_me_agent.add_output("contextual_answer")
ask_me_agent.add_output("source_explanation")
ask_me_agent.add_output("followup_prompt")
ask_me_agent.add_output("audio_narration")
