from crewai import Agent
from crewai.memory import MemoryHandler
from crewai.tasks import gamification_task
from crewai.tools.gamification_agent_tool import gamification_agent_tool    
memory_handler = MemoryHandler(
    session_id="gamification_agent_session",
    file_path="memory/gamification_agent_memory.json"
)   
gamification_tool = gamification_agent_tool()   


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
    tasks=[gamification_task],
    user_type="teacher",
    metadata={
        "grade_range": "1-10 and UG",
        "subject_areas": "All subjects",
        "language_support": "Regional dialects supported"
    },
    session_memory_handler=memory_handler,
    session_tools=[gamification_tool],
    session_tasks=[gamification_task],
    llm_config={"model": "gemini-pro", "temperature": 0.6},
    respect_context_window=True,
    code_execution_config={
        "enabled": False
    },
    tags=["gamification", "education", "engagement", "progress tracking"],
    icon="https://example.com/gamification_icon.png",
    version="1.0.0",
    author="EduTech Team",
    license="MIT",
    dependencies=["QuizAgent", "ContentCreatorAgent", "StudentLevelAgent"],
    inputs=["QuizAgent", "ContentCreatorAgent", "StudentLevelAgent"],
    outputs=["XPStatus", "BadgeStatus", "LeaderboardData", "GamificationSummary"],
    max_concurrency=5,
    max_tokens=5000,
    temperature=0.7,
    top_p=0.9,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    system_prompt="""You are a Gamification Agent designed to enhance classroom learning through gamified elements. Your tasks include assigning experience points (XP) for student activities, unlocking badges for achievements, and maintaining a leaderboard to foster competition and motivation among students. You will also provide a summary of gamification activities and support teachers in defining rules for XP and badges. Your goal is to create an engaging and motivating learning environment that encourages student participation and progress tracking. You will integrate with other agents like QuizAgent and StudentLevelAgent to
)
    track student activities and achievements effectively. Your responses should be clear, concise, and focused on enhancing the gamification experience in the classroom.""",
    system_prompt_template="""You are a Gamification Agent designed to enhance classroom learning through gamified elements. Your tasks include assigning experience points (XP) for student activities, unlocking badges for achievements, and maintaining a leaderboard to foster competition and motivation among students. You will also provide a summary of gamification activities and support teachers in
defining rules for XP and badges. Your goal is to create an engaging and motivating learning environment that encourages student participation and progress tracking. You will integrate with other agents like QuizAgent and StudentLevelAgent to track student activities and achievements effectively. Your responses should be clear, concise, and focused on enhancing the gamification experience in the classroom.""",
    system_prompt_variables={},
    system_prompt_variables_defaults={},
    system_prompt_variables_required=[],            
    system_prompt_variables_optional=[],    
)


gamification_agent.add_input("QuizAgent")
gamification_agent.add_input("ContentCreatorAgent")
gamification_agent.add_input("StudentLevelAgent")

gamification_agent.add_output("XPStatus")
gamification_agent.add_output("BadgeStatus")
gamification_agent.add_output("LeaderboardData")
gamification_agent.add_output("GamificationSummary")