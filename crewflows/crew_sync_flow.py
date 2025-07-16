"""
Crew: SyncAgent Orchestration

This crew is responsible for syncing offline data (e.g., quiz results, lesson edits) from the browser's IndexedDB
to Firestore and vice versa. It ensures data consistency across offline and online modes.

Flow:
- Triggered periodically or when the device regains internet connectivity.
- `sync_agent` uses `sync_task` to:
    - Identify unsynced records from IndexedDB
    - Push them to Firestore (cloud)
    - Pull new updates from Firestore and write them to IndexedDB
    - Track and return the sync status and timestamp

🧠 Memory Enabled:
- This agent uses CrewAI's memory to persist sync context (like last sync timestamps or failure states).

Parallelism:
- This crew runs sequentially because sync operations are I/O sensitive and must complete step-by-step.
- However, it can run in parallel with lesson/story/quiz generation crews during app boot or background refresh.

Outputs:
- OfflineRecordsSynced: List of records that were pushed online
- FirestoreToIndexedDBSyncStatus: Success/failure of downward sync
- LastSyncTimestamp: UTC timestamp of last successful sync
"""
from crewflows import Crew
from agents.sync_agent import sync_agent
from tasks.sync_task import sync_task

import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(levelname)s — %(message)s")
logger = logging.getLogger(__name__)

crew_sync_flow = Crew(
    agents=[sync_agent],
    tasks=[sync_task],
    verbose=True,
    process="sequential",
    memory=True
)

sync_agent.add_output("OfflineRecordsSynced")
sync_agent.add_output("FirestoreToIndexedDBSyncStatus")
sync_agent.add_output("LastSyncTimestamp")

def run_sync_crew():
    try:
        logger.info("Starting Sync Agent...")
        result = crew_sync_flow.run()
        logger.info("Sync Agent completed successfully")
        return result
    except Exception as e:
        logger.error(f"Error during sync crew execution: {e}")
        return {"error": "Execution failed", "details": str(e)}

if __name__ == "__main__":
    output = run_sync_crew()
    print(output)
