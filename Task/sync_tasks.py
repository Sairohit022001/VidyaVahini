from crewai import Task
from pydantic import BaseModel, Field

class SyncStatusOutput(BaseModel):
    synced: bool = Field(..., description="Was sync successful?")
    offline_records_uploaded: int = Field(..., description="How many offline items were pushed?")
    updates_downloaded: int = Field(..., description="How many updates were pulled from server?")
    timestamp: str = Field(..., description="Time of last sync")

generate_sync_task = Task(
    name="Handle Offline-Online Sync",
    description=(
        "1. Detect changes made while offline using local IndexedDB.\n"
        "2. Push unsynced changes (e.g. notes, quiz results) to Firestore.\n"
        "3. Pull latest updates from Firestore to IndexedDB.\n"
        "4. Perform two-way conflict resolution if data mismatch exists.\n"
        "5. Track and record sync timestamp for next sync.\n"
        "6. Maintain user data integrity in offline-first architecture.\n"
        "7. Ensure that no student/teacher data is lost across sessions.\n"
        "8. Run on reconnection or via manual trigger from dashboard.\n"
        "9. Log sync errors and retry logic if sync fails.\n"
        "10. Return JSON summary of sync status and statistics."
    ),
    expected_output=SyncStatusOutput,
    output_json=True,
    context_injection=True,
    verbose=True
)
