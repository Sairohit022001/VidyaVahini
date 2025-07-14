from crewai import Task
from pydantic import BaseModel, Field
from typing import List, Optional

class CoursePlanSchema(BaseModel):
    current_topic: str = Field(..., description="Current topic student is learning")
    recommended_topic: str = Field(..., description="AI-suggested next topic for continuation")
    reason: str = Field(..., description="Justification for recommending this topic")
    difficulty_adjustment: str = Field(..., description="How difficulty was adapted (up/down/same)")
    level: str = Field(..., description="Recommended topic level (Beginner / Medium / Advanced)")
    suggested_agents: List[str] = Field(default=["QuizAgent", "VisualAgent"], description="Other agents to be called next")
    linked_materials: Optional[List[str]] = Field(default=[], description="List of URLs, PDFs, or links for suggested topic")

generate_course_plan_task = Task(
    name="Generate Next Course Topic",
    description=(
        "Given a student's performance data (quiz scores, current topic), recommend the next topic. "
        "Consider pacing, curriculum flow, dependencies, and performance. Justify why this topic is ideal. "
        "Mention whether difficulty should be increased, reduced, or kept the same. "
        "Return a JSON following CoursePlanSchema with clarity."
    ),
    expected_output=CoursePlanSchema,
    output_json=True,
    context_injection=True
)