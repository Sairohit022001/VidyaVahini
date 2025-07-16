from crewflows import Agent
from tools.sync_tool import SyncTool
from tasks.sync_tasks import run_sync_task
from crewflows.memory.local_memory_handler import LocalMemoryHandler
     

memory_handler = LocalMemoryHandler(
    session_id="sync_agent_session",
    file_path="memory/sync_agent_memory.json"
)       

    


sync_agent = Agent(
    name="SyncAgent",
    role="Offline-aware synchronization handler",
    goal="""
1. Enable real-time synchronization between local IndexedDB and Firestore backend.
2. Handle offline-to-online transitions gracefully.
3. Maintain a sync queue for data generated while offline.
4. Prevent data duplication or overwrites via conflict resolution.
5. Track sync status visibly on the teacher dashboard.
6. Sync lesson plans, quiz scores, and user activity.
7. Alert teachers if students remain unsynced for long durations.
8. Support auto-sync and manual sync trigger modes.
9. Minimize network usage by syncing diffs, not full data.
10. Work in the background without interrupting the teaching flow.
""",
    backstory="""
1. Designed for rural classrooms with inconsistent connectivity.
2. Empowers teachers to use AI tools regardless of internet strength.
3. Keeps local and cloud databases consistently up to date.
4. Ensures student learning records aren't lost offline.
5. Provides visual feedback about sync status.
6. Uses conflict-free replicated data types where needed.
7. Developed with IndexedDB and Firestore sync bridge logic.
8. Integrates seamlessly with content agents and dashboards.
9. Supports audio, PDF, and JSON data formats.
10. A cornerstone agent for offline-first architecture of VidyaVāhinī.
""",
    tools=[SyncTool],
    tasks=[run_sync_task],
    memory=True,
    memory_handler=memory_handler,
    allow_delegation=True,
    verbose=True,
    llm_config={"model": "gemini-pro", "temperature": 0.7, "max_tokens": 2048},
    respect_context_window=True,
    code_execution_config={"enabled": True,"executor_type": "kirchhoff-async"},
    user_type="teacher",
    metadata={
        "grade_range": "1-10 and UG",
        "access": "teacher_only",
        "delegates_to": ["LessonPlannerAgent", "StoryTellerAgent", "QuizAgent"]
    }
)

sync_agent.add_input("OfflineLessonUpdates")
sync_agent.add_input("StudentInteractionData")
sync_agent.add_output("FirestoreSyncStatus")
sync_agent.add_output("OfflineUpdatesPending")
sync_agent.add_output("IndexedDBData")