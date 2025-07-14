from crewai import Task
from pydantic import BaseModel, Field
from typing import List

class GamificationOutput(BaseModel):
    xp_distribution: dict
    badge_earned: List[str]
    leaderboard: List[str]

generate_gamification_logic_task = Task(
    name="Generate Gamification Logic",
    description=(
        "1. Analyze student engagement and participation.\n"
        "2. Assign XP points based on activity (e.g. quiz, story).\n"
        "3. Define badge criteria for completion milestones.\n"
        "4. Generate weekly leaderboard based on XP.\n"
        "5. Encourage participation via incentives.\n"
        "6. Promote healthy competition within the class.\n"
        "7. Adjust XP dynamically based on difficulty and pace.\n"
        "8. Reset leaderboard at defined intervals.\n"
        "9. Sync gamification metrics to dashboard.\n"
        "10. Return gamified summary for teacher + public view."
    ),
    expected_output=GamificationOutput,
    output_json=True,
    context_injection=True,
    verbose=True
)