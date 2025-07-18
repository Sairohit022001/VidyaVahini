from pydantic import BaseModel, Field, ValidationError
from typing import List, Dict, Any
import asyncio

# Schema definition
class DashboardMetrics(BaseModel):
    quiz_completion_rate: float = Field(..., description="Percentage of students who completed recent quizzes")
    lesson_view_rate: float = Field(..., description="Percentage of students who viewed the last 3 lessons")
    dropout_alerts: List[str] = Field(..., description="List of student IDs likely to drop based on inactivity trends")
    flagged_students: List[str] = Field(..., description="Students flagged for performance drop, inactivity, or alerts")

    class Config:
        title = "Teacher Dashboard Analytics"
        description = "Weekly engagement metrics for each class used by teacher dashboard and predictive agents"

# Task class
class GenerateDashboardMetricsTask:
    name = "Generate Teacher Dashboard Metrics"
    description = (
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
    )
    expected_output = DashboardMetrics
    output_json = True
    context_injection = True
    verbose = True
    output_file = "outputs/dashboard_metrics_{timestamp}.json"
    guardrails = {
        "retry_on_fail": 1,
        "fallback_response": {
            "quiz_completion_rate": 0.0,
            "lesson_view_rate": 0.0,
            "dropout_alerts": [],
            "flagged_students": []
        }
    }
    metadata = {
        "agent": "TeacherDashboardAgent",
        "access": "teacher_only",
        "downstream": ["PredictiveAnalyticsAgent", "CoursePlannerAgent", "StudentLevelAgent"],
        "triggers": ["weekly", "manual_refresh"],
        "ui_component": "Teacher Dashboard – Analytics Widget"
    }

    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Async run method to calculate and return teacher dashboard analytics metrics.

        Args:
            inputs (dict): Should contain student quiz data, lesson views, and activity logs.

        Returns:
            dict: JSON compatible with DashboardMetrics schema.
        """
        try:
            await asyncio.sleep(0.1)  # Simulate async processing / data fetch
            
            # Extract or simulate data from inputs
            quiz_data = inputs.get("quiz_data", {})
            lesson_views = inputs.get("lesson_views", {})
            activity_logs = inputs.get("activity_logs", {})

            total_students = quiz_data.get("total_students", 1) or 1
            completed_quizzes = quiz_data.get("completed_quizzes", 0)
            quiz_completion_rate = completed_quizzes / total_students * 100

            total_lessons = 3
            viewed_lessons_count = lesson_views.get("viewed_last_3", 0)
            lesson_view_rate = viewed_lessons_count / total_students * 100

            # Simple heuristics for dropout alerts and flagged students
            dropout_alerts: List[str] = []
            flagged_students: List[str] = []
            inactivity_threshold_days = 3

            for student_id, last_active_days_ago in activity_logs.items():
                if last_active_days_ago > inactivity_threshold_days:
                    dropout_alerts.append(student_id)
                # Placeholder for flagged students logic

            metrics = DashboardMetrics(
                quiz_completion_rate=quiz_completion_rate,
                lesson_view_rate=lesson_view_rate,
                dropout_alerts=dropout_alerts,
                flagged_students=flagged_students,
            )
            return metrics.dict()

        except ValidationError as ve:
            if self.verbose:
                print(f"Validation error in DashboardMetrics: {ve}")
            return self.guardrails.get("fallback_response", {})
        except Exception as e:
            if self.verbose:
                print(f"Error in GenerateDashboardMetricsTask.run: {e}")
            fallback = self.guardrails.get("fallback_response", {})
            return fallback

# Instantiate task for agent usage
generate_dashboard_metrics_task = GenerateDashboardMetricsTask()
