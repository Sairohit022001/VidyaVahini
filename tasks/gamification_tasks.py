from tasks import Task
from pydantic import BaseModel, Field
from typing import List, Optional

class GamificationOutput(BaseModel):
    xp_awarded: int = Field(..., description="Total XP awarded to the student")
    badge_unlocked: Optional[str] = Field(None, description="Badge name if student unlocked one")
    leaderboard_position: Optional[int] = Field(None, description="Updated leaderboard rank")
    quiz_score: int = Field(..., description="Latest quiz score")
    student_id: str = Field(..., description="Student identifier")

generate_gamification_task = Task(
    name="Update Gamification Progress",
    description=(
        "Accept student's quiz score, time spent, and participation data.\n"
        "Assign XP based on score thresholds.\n"
        "Award badges if milestones achieved.\n"
        "Recalculate leaderboard positions.\n"
        "Store progress for each student.\n"
        "Push update to student's dashboard.\n"
        "Track weekly and monthly streaks.\n"
        "Suggest goals or challenges if lagging.\n"
        "Output must be JSON with all required metrics.\n"
        "Trigger animations if badges earned."
    ),
    expected_output=GamificationOutput,
    output_json=True,
    context_injection=True,
    verbose=True,
    output_file="outputs/gamification_{timestamp}.json",
    guardrails={
        "retry_on_fail": 2,
        "fallback_response": {
            "xp_awarded": 0,
            "badge_unlocked": None,
            "leaderboard_position": None,
            "quiz_score": 0,
            "student_id": "unknown"
        }
    },
    metadata={
        "agent": "GamificationAgent",
        "access": "student_only",
        "downstream": ["DashboardAgent"],
        "triggers": ["on_quiz_submission"]
    }
)
