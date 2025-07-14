from crewai import Task
from pydantic import BaseModel, Field
from typing import List

class DashboardMetrics(BaseModel):
    quiz_completion_rate: float
    lesson_view_rate: float
    dropout_alerts: List[str]
    flagged_students: List[str]

generate_dashboard_metrics_task = Task(
    name="Generate Teacher Dashboard Metrics",
    description=(
        "1. Calculate quiz participation and completion rates.\n"
        "2. Analyze lesson view activity over the past 7 days.\n"
        "3. Detect students with 3+ days of inactivity.\n"
        "4. Generate early dropout warnings for flagged students.\n"
        "5. Track performance trends to assist CoursePlannerAgent.\n"
        "6. Compile a list of students needing attention.\n"
        "7. Monitor overall engagement class-wide.\n"
        "8. Output metrics for UI display on teacher dashboard.\n"
        "9. Feed insights into PredictiveAnalyticsAgent.\n"
        "10. Run weekly or on-demand via dashboard refresh."
    ),
    expected_output=DashboardMetrics,
    output_json=True,
    context_injection=True,
    verbose=True
)
