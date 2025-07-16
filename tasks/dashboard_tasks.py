from tasks import Task
from pydantic import BaseModel, Field
from typing import List

# Step 1: Define the structured schema for dashboard metrics
class DashboardMetrics(BaseModel):
    quiz_completion_rate: float = Field(..., description="Percentage of students who completed recent quizzes")
    lesson_view_rate: float = Field(..., description="Percentage of students who viewed the last 3 lessons")
    dropout_alerts: List[str] = Field(..., description="List of student IDs likely to drop based on inactivity trends")
    flagged_students: List[str] = Field(..., description="Students flagged for performance drop, inactivity, or alerts")

    class Config:
        title = "Teacher Dashboard Analytics"
        description = "Weekly engagement metrics for each class used by teacher dashboard and predictive agents"

# Step 2: Define the Task using CrewAI
generate_dashboard_metrics_task = Task(
    name="Generate Teacher Dashboard Metrics",
    description=(
        "Calculate quiz participation and completion percentages for each class.\n"
        "Analyze student activity for lesson views over the past 7 days.\n"
        "Identify students with >3 days inactivity and generate alerts.\n"
        "Flag students with declining performance for review.\n"
        "Detect possible early dropout patterns using heuristics.\n"
        "Return structured flags usable by PredictiveAnalyticsAgent.\n"
        "Compile student engagement summaries for teacher UI.\n"
        "Include metrics for CoursePlannerAgent and StudentLevelAgent.\n"
        "Trigger updates weekly or manually via dashboard reload.\n"
        "Return all data in JSON using DashboardMetrics schema."
    ),
    expected_output=DashboardMetrics,
    output_json=True,
    context_injection=True,
    verbose=True,
    output_file="outputs/dashboard_metrics_{timestamp}.json",
    guardrails={
        "retry_on_fail": 1,
        "fallback_response": {
            "quiz_completion_rate": 0.0,
            "lesson_view_rate": 0.0,
            "dropout_alerts": [],
            "flagged_students": []
        }
    },
    metadata={
        "agent": "TeacherDashboardAgent",
        "access": "teacher_only",
        "downstream": ["PredictiveAnalyticsAgent", "CoursePlannerAgent", "StudentLevelAgent"],
        "triggers": ["weekly", "manual_refresh"],
        "ui_component": "Teacher Dashboard – Analytics Widget"
    }
)