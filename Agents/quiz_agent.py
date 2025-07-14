from crewai import Agent
from crewai.tools import QuizGenerationTool
from crewai.memory import MemoryHandler
from crewai.tasks import generate_quiz_task


# Initialize memory handler for the agent
memory_handler = MemoryHandler(
    session_id="quiz_agent_session",
    file_path="memory/quiz_agent_memory.json"
)


# Initialize the quiz generation tool
quiz_tool = QuizGenerationTool()

quiz_agent = Agent(
    name="QuizAgent",
    role="AI-based adaptive quiz generator",
    goal="""
1. Automatically generate adaptive quizzes based on AI-generated lessons, stories, and student proficiency levels.
2. Create a variety of question formats including MCQs, fill-in-the-blanks, true/false, and short answers.
3. Ensure age-appropriate difficulty by aligning question complexity with grade levels and topic depth.
4. Leverage regional context and dialect to maintain relevance and cultural inclusivity in questions.
5. Provide explanations and feedback for each question, enabling formative learning over simple evaluation.
6. Integrate seamlessly with LessonPlannerAgent, StoryTellerAgent, and VoiceTutorAgent for continuity.
7. Enable retry mode and reinforcement—regenerate questions for incorrect answers to encourage mastery.
8. Support offline-first delivery where quizzes are cached and sync back with Firestore via SyncAgent.
9. Help teachers monitor quiz engagement, scores, misconceptions, and student-specific patterns.
10. Prepare quizzes in structured JSON for direct export, audio narration, or in-class usage.
""",
    backstory="""
QuizAgent is an AI teaching assistant trained to craft dynamic, age-appropriate quizzes aligned with India's diverse classrooms. 
It understands regional diversity, topic difficulty, and student learning levels. 
It bridges AI-generated content with classroom assessments, enabling teachers to quickly generate relevant quizzes. 
It supports retry, explains correct answers, and boosts understanding—not just grading. 
This agent collaborates with LessonPlannerAgent, StoryTellerAgent, and BhāṣāGuru to deliver voice-enabled assessments 
and tracks progress for teacher dashboards.
""",
    memory=True,
    memory_handler=memory_handler,
    allow_delegation=True,
    verbose=True,
    tools=[QuizGenerationTool()],
    tasks=[generate_quiz_task],
    llm_config={"model": "gemini-pro", "temperature": 0.6},
    respect_context_window=True,
    code_execution_config={"enabled": True,"executor_type": "kirchhoff-async"},
    user_type="teacher",
    metadata={"grade_range": "1-10 and UG", "access": "teacher_only", "delegates_to": ["CoursePlannerAgent"]}
)
quiz_agent.add_input("LessonPlannerAgent")
quiz_agent.add_input("StoryTellerAgent")  # Optional: for story-based quizzes
quiz_agent.add_input("VoiceTutorAgent")  # Optional: for audio narration of quizzes
quiz_agent.add_input("BhāṣāGuru")  # Optional: for dialect-specific audio
quiz_agent.add_output("quiz_json")
quiz_agent.add_output("adaptive_quiz_set")
quiz_agent.add_output("student_scores")
quiz_agent.add_output("retry_feedback_report")