from crewai import Task
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class ClassAnalyticsOutputSchema(BaseModel):
    average_score: float = Field(..., description="Average score of the class for the quiz")
    top_performers: List[str] = Field(..., description="List of top-performing students")
    weak_areas: List[str] = Field(..., description="Concepts or topics where students performed poorly")
    recommendations: Dict[str, Any] = Field(
        ...,
        description=(
            "Personalized recommendations per student and general suggestions for lesson planning, "
            "including chapters to focus on and concepts to re-explain"
        )
    )

generate_class_analytics_task = Task(
    name="GenerateClassAnalytics",
    description=(
        "Analyze quiz results to produce detailed class-level and individual student analytics for each quiz. "
        "Outputs include average scores, identification of top performers and weak areas, personalized recommendations "
        "to guide lesson planning, and suggestions for chapters or concepts requiring re-explanation. "
        "Also compares performance trends across multiple quizzes."
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
            "recommendations": {}
        }
    },
    metadata={
        "agent": "AnalyticsAgent",
        "access": "teacher_only",
        "downstream": ["LessonPlannerAgent", "TeacherDashboardAgent"],
        "triggers": ["on_quiz_completion", "periodic_review"]
    },
    tool="predictive_analytics_tool"
)