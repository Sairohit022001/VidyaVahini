from crewai import Task
from pydantic import BaseModel, Field
from typing import List

class ClassAnalyticsOutputSchema(BaseModel):
    average_score: float = Field(..., description="Average score of the class across the quiz")
    top_performers: List[str] = Field(..., description="List of top-performing student IDs or names")
    weak_areas: List[str] = Field(..., description="List of commonly misunderstood topics or concepts")
    lesson_plan_suggestions: List[str] = Field(
        ...,
        description="Chapters or concepts to re-emphasize in future lessons"
    )

generate_class_analytics_task = Task(
    name="GenerateClassAnalytics",
    description=(
        "Analyze overall class quiz results to extract aggregate performance indicators such as average score, "
        "top performers, and weak areas. Generate actionable lesson planning suggestions for teachers. "
        "Focus only on class-level trends without diving into individual student analytics."
    ),
    inputs=["quiz_results"],
    expected_output=ClassAnalyticsOutputSchema,
    output_json=True,
    context_injection=True,
    verbose=True,
    output_file="outputs/class_analytics_{timestamp}.json",
    guardrails={
        "retry_on_fail": 1,
        "fallback_response": {
            "average_score": 0.0,
            "top_performers": [],
            "weak_areas": [],
            "lesson_plan_suggestions": []
        }
    },
    metadata={
        "agent": "PredictiveAnalyticsAgent",
        "access": "teacher_only",
        "downstream": ["LessonPlannerAgent", "TeacherDashboardAgent"],
        "triggers": ["on_quiz_completion", "periodic_review"]
    },
    tool="predictive_analytics_tool"
)
