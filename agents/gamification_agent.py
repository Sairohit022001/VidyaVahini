from crewflows import Agent
from crewflows.memory.local_memory_handler import LocalMemoryHandler
from tasks.gamification_tasks import generate_gamification_task
from tools.gamification_tool import GamificationTool

memory_handler = LocalMemoryHandler(
    session_id="gamification_agent_session",
    file_path="memory/gamification_agent_memory.json"
)

gamification_tool = GamificationTool()

gamification_agent = Agent(
    name="GamificationAgent",
    role="Gamify classroom learning and progress tracking",
    goal="""
1. Assign XP based on quiz participation and lesson interaction.
2. Unlock badges for milestones or consistency.
3. Power a student leaderboard visible to all.
4. Enable teachers to define XP and badge rules.
5. Promote engagement via weekly/monthly challenges.
6. Track activity streaks and reward improvement.
7. Support gamified feedback in the student dashboard.
8. Provide visual celebration of achievements.
9. Encourage collaborative learning via team events.
10. Reinforce habit-building and intrinsic motivation.
""",
    backstory="""
1. Inspired by mobile learning games and habit trackers.
2. Designed to engage students through playful reward systems.
3. Visualizes progress in XP bars and badge sets.
4. Integrates with QuizAgent and StudentLevelAgent.
5. Teachers configure custom thresholds and themes.
6. Gamified learning increases retention and participation.
7. Sends updates to dashboards in real-time.
8. Offers anonymous or named leaderboard modes.
9. Especially impactful in rural classrooms for boosting morale.
10. Powered by education psychology and feedback loops.
""",
    memory=True,
    memory_handler=memory_handler,
    allow_delegation=True,
    verbose=True,
    tools=[gamification_tool],
    tasks=[generate_gamification_task],
    user_type="teacher",
    metadata={
        "grade_range": "1-10 and UG",
        "subject_areas": "All subjects",
        "language_support": "Regional dialects supported",
        "dependencies": ["QuizAgent", "ContentCreatorAgent", "StudentLevelAgent"],
        "tags": ["gamification", "education", "engagement", "progress tracking"],
        "icon": "https://example.com/gamification_icon.png",
        "version": "1.0.0",
        "author": "EduTech Team",
        "license": "MIT"
    },
    llm_config={"model": "gemini-pro", "temperature": 0.6},
    respect_context_window=True,
    code_execution_config={
        "enabled": True,
        "executor_type": "kirchhoff-async"
    }
)

# Register inputs
gamification_agent.add_input("QuizAgent")
gamification_agent.add_input("ContentCreatorAgent")
gamification_agent.add_input("StudentLevelAgent")

# Register outputs
gamification_agent.add_output("XPStatus")
gamification_agent.add_output("BadgeStatus")
gamification_agent.add_output("LeaderboardData")
gamification_agent.add_output("GamificationSummary")
