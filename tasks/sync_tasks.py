from tasks import Task
from pydantic import BaseModel, Field
from typing import List

class SyncStatusSchema(BaseModel):
    firestore_status: str = Field(..., description="Status of Firestore sync: Synced / Error / Offline")
    indexeddb_status: str = Field(..., description="IndexedDB local cache sync: Synced / Error / Stale")
    last_sync_timestamp: str = Field(..., description="Timestamp of last sync completion")
    offline_students: List[str] = Field(default=[], description="List of students still offline")

run_sync_task = Task(
    name="Sync Firestore with IndexedDB",
    description=(
        "Trigger Firestore ↔ IndexedDB sync operation.\n"
        "Fetch all updated lessons, quizzes, and student data.\n"
        "Push unsynced local data from IndexedDB to Firestore.\n"
        "Log student offline statuses for last 24 hrs.\n"
        "Maintain offline-first compatibility.\n"
        "Run on dashboard open or every 5 minutes.\n"
        "Validate if Firestore rules permit writes.\n"
        "Catch sync errors and mark unsynced records.\n"
        "Track last success timestamp.\n"
        "Output SyncStatusSchema JSON for UI and logs."
    ),
    expected_output=SyncStatusSchema,
    output_json=True,
    context_injection=True,
    verbose=True,
    output_file="outputs/sync_status_{timestamp}.json",
    guardrails={
        "retry_on_fail": 1,
        "fallback_response": {
            "firestore_status": "Error",
            "indexeddb_status": "Stale",
            "last_sync_timestamp": "unknown",
            "offline_students": []
        }
    },
    metadata={
        "agent": "SyncAgent",
        "access": "teacher_and_student",
        "downstream": ["TeacherDashboardAgent", "CoursePlannerAgent"],
        "triggers": ["on_dashboard_load", "on_app_start"]
    }
)

