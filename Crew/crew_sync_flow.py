from crewai import Crew
from agents.sync_agent import sync_agent
from tasks.sync_task import sync_task

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