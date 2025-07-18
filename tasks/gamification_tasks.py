# tasks/gamification_tasks.py

from pydantic import BaseModel, Field
from typing import Optional
from base.agent_base import BaseAgent
from crewai import Task

class GamificationOutput(BaseModel):
    student_id: str = Field(..., description="Unique identifier for the student")
    xp_awarded: int = Field(..., description="Experience points awarded")
    badge_unlocked: Optional[str] = Field(None, description="Name of badge unlocked, if any")
    leaderboard_position: Optional[int] = Field(None, description="Current leaderboard rank")
    quiz_score: int = Field(..., description="Score obtained in the quiz")

def generate_gamification_task(agent: BaseAgent) -> Task:
    return Task(
        name="Generate Gamification Features",
        description=(
            "Analyze student interaction data and suggest gamified learning modules. "
            "Use principles of game design to increase student engagement and retention. "
            "Focus on regional relevance, age-appropriateness, and motivation mechanics."
        ),
        expected_output=GamificationOutput,
        agent=agent,
        async_execution=False,
        output_file="outputs/gamification_{timestamp}.json"
    )
