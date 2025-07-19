from crewflows import Agent
from crewflows.memory.local_memory_handler import LocalMemoryHandler
from tasks.gamification_tasks import generate_gamification_task
from tools.gamification_tool import GamificationTool
from langchain_google_genai import ChatGoogleGenerativeAI

memory_handler = LocalMemoryHandler(
    session_id="gamification_agent_session",
    file_path="memory/gamification_agent_memory.json"
)

gamification_tool = GamificationTool()

class GamificationAgentWrapper(Agent):
    def __init__(self, **kwargs):
        # Provide default goal if not passed
        if 'goal' not in kwargs:
            kwargs['goal'] = (
                "Assign XP based on quiz participation and lesson interaction; "
                "unlock badges for milestones; track leaderboard positions; "
                "promote student engagement via challenges and streak tracking."
            )
        # Remove the function from the tasks list
        if 'tasks' in kwargs and isinstance(kwargs['tasks'], list):
            kwargs['tasks'] = [task for task in kwargs['tasks'] if not callable(task)]

        super().__init__(**kwargs)

    async def process(self, inputs: dict):
        try:
            # Call the function to get a task instance
            # Assuming 'self' is the agent instance needed by generate_gamification_task
            task_instance = generate_gamification_task(agent=self)

            # Ensure the task instance has a callable execute or run method
            if hasattr(task_instance, "execute") and callable(task_instance.execute):
                # Call the execute method on the task instance
                # crewai.Task's execute method might not be async by default, check its definition
                result = task_instance.execute(inputs) # Or await task_instance.execute(inputs) if it's async
                return result
            elif hasattr(task_instance, "run") and callable(task_instance.run):
                 # If it's a custom task with a run method (like your BaseTask)
                maybe_coro = task_instance.run(inputs)
                if hasattr(maybe_coro, "__await__"):
                     result = await maybe_coro
                else:
                     result = maybe_coro
                return result
            else:
                return {"error": "Generated task instance has no callable 'execute' or 'run' method."}

        except Exception as e:
            return {"error": f"GamificationAgent process() failed: {str(e)}"}

gamification_agent = GamificationAgentWrapper(
    name="GamificationAgent",
    role="""
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
    tasks=[], # Removed the function from the tasks list
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
    llm=ChatGoogleGenerativeAI(
        model="models/gemini-2.5-pro",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.3
    ),
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
