from crewai import Task
from pydantic import BaseModel, Field
from typing import List

class StudentAnalyticsOutputSchema(BaseModel):
    student_id: str = Field(..., description="Unique identifier or name of the student")
    strengths: List[str] = Field(..., description="Topics or concepts the student performs well in")
    weaknesses: List[str] = Field(..., description="Topics where the student struggles")
    recommendations: List[str] = Field(..., description="Suggested actions or topics to revise")
    progress_score: float = Field(..., description="Normalized progress score or learning growth")

generate_student_analytics_task = Task(
    name="GenerateStudentLevelAnalytics",
    description=(
        "Given an individual student's performance history, identify their strengths, weaknesses, "
        "and generate personalized recommendations. Track academic progress over time and suggest "
        "specific learning interventions."
    ),
    inputs=["student_performance"],
    expected_output=StudentAnalyticsOutputSchema,
    output_json=True,
    context_injection=True,
    verbose=True,
    output_file="outputs/student_analytics_{timestamp}.json",
    guardrails={
        "retry_on_fail": 1,
        "fallback_response": {
            "student_id": "unknown",
            "strengths": [],
            "weaknesses": [],
            "recommendations": [],
            "progress_score": 0.0
        }
    },
    metadata={
        "agent": "StudentLevelAnalyticsAgent",
        "access": "teacher_only",
        "triggers": ["on_student_dashboard_request"]
    },
    tool="student_level_analytics_tool"
)
