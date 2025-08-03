from crewflows import Agent
from tools.sync_tool import SyncTool
from tasks.sync_tasks import SyncTask
from crewflows.memory.local_memory_handler import LocalMemoryHandler
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Any, Dict
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Load environment variables (.env must include GOOGLE_APPLICATION_CREDENTIALS and GEMINI_API_KEY)
load_dotenv()

# Initialize Firebase Firestore client globally
FIRESTORE_CREDENTIAL_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not FIRESTORE_CREDENTIAL_PATH:
    raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS must be set in environment variables")

if not firebase_admin._apps:
    cred = credentials.Certificate(FIRESTORE_CREDENTIAL_PATH)
    firebase_admin.initialize_app(cred)

firestore_client = firestore.client()

# Minimal IndexedDB client stub: replace with actual implementation if available
class IndexedDBMock:
    def put(self, *args, **kwargs):
        pass
    def get(self, *args, **kwargs):
        return {}
    def delete(self, *args, **kwargs):
        pass
    # Add other necessary methods expected by SyncTool here

indexeddb_client = IndexedDBMock()

# Memory handler
memory_handler = LocalMemoryHandler(
    session_id="sync_agent_session",
    file_path="memory/sync_agent_memory.json"
)


class SyncAgentWrapper(Agent):
    def __init__(self, *args, name: str = "sync_agent", **kwargs):
        # Instantiate SyncTool with required clients
        self.sync_tool = SyncTool(firestore_client, indexeddb_client)
        self.sync_task = SyncTask()

        super().__init__(
            *args,
            name=name,
            role=(
                "1. Enable real-time synchronization between local IndexedDB and Firestore backend.\n"
                "2. Handle offline-to-online transitions gracefully.\n"
                "3. Maintain a sync queue for data generated while offline.\n"
                "4. Prevent data duplication or overwrites via conflict resolution.\n"
                "5. Track sync status visibly on the teacher dashboard.\n"
                "6. Sync lesson plans, quiz scores, and user activity.\n"
                "7. Alert teachers if students remain unsynced for long durations.\n"
                "8. Support auto-sync and manual sync trigger modes.\n"
                "9. Minimize network usage by syncing diffs, not full data.\n"
                "10. Work in the background without interrupting the teaching flow."
            ),
            goal=(
                "Provide robust offline-first and cross-device data synchronization for lessons, quizzes, "
                "and user actions in the VidyaVāhinī platform."
            ),
            tools=[self.sync_tool],
            tasks=[self.sync_task],
            memory=True,
            memory_handler=memory_handler,
            allow_delegation=True,
            verbose=True,
            llm=ChatGoogleGenerativeAI(
                model="models/gemini-2.5-pro",
                google_api_key=os.getenv("GEMINI_API_KEY"),
                temperature=0.3
            ),
            respect_context_window=True,
            code_execution_config={"enabled": True, "executor_type": "kirchhoff-async"},
            user_type="teacher",
            metadata={
                "grade_range": "1-10 and UG",
                "access": "teacher_only",
                "delegates_to": [
                    "lesson_planner_agent",
                    "story_teller_agent",
                    "quiz_agent"
                ],
            },
            **kwargs
        )
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    async def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Asynchronously process sync-related inputs.

        Args:
            inputs (Dict[str, Any]): Should include offline lesson updates, student interaction data, etc.

        Returns:
            Dict[str, Any]: Sync status, pending updates, and databases.
        """
        try:
            result = await self.sync_task.run(inputs)
            return result
        except Exception as e:
            return {"error": f"SyncAgent process() failed: {str(e)}"}


# Instantiate the SyncAgent
sync_agent = SyncAgentWrapper()

# Register expected inputs
sync_agent.add_input("OfflineLessonUpdates")
sync_agent.add_input("StudentInteractionData")

# Register expected outputs
sync_agent.add_output("FirestoreSyncStatus")
sync_agent.add_output("OfflineUpdatesPending")
sync_agent.add_output("IndexedDBData")
