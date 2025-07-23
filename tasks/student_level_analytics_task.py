from tasks.task import Task
from pydantic import BaseModel, Field
from typing import List

class StudentAnalyticsOutputSchema(BaseModel):
    student_id: str = Field(..., description="Unique identifier or name of the student")
    strengths: List[str] = Field(..., description="Topics or concepts the student performs well in")
    weaknesses: List[str] = Field(..., description="Topics where the student struggles")
    recommendations: List[str] = Field(..., description="Suggested actions or topics to revise")
    progress_score: float = Field(..., description="Normalized progress score or learning growth")

class StudentLevelAnalyticsTask(Task):
    def __init__(self):
        super().__init__(
            name="StudentLevelAnalyticsTask",
            description=(
                "Analyze student quiz and activity data to provide personalized insights, "
                "strengths, weaknesses, recommendations, and progress scores."
            )
        )
        self.inputs = ["student_performance"]
        self.expected_output = StudentAnalyticsOutputSchema
        self.output_json = True
        self.context_injection = True
        self.verbose = True
        self.output_file = "outputs/student_analytics_{timestamp}.json"
        self.guardrails = {
            "retry_on_fail": 1,
            "fallback_response": {
                "student_id": "unknown",
                "strengths": [],
                "weaknesses": [],
                "recommendations": [],
                "progress_score": 0.0,
            }
        }
        self.metadata = {
            "agent": "StudentLevelAnalyticsAgent",
            "access": "teacher_only",
            "triggers": ["on_student_dashboard_request"],
        }

    async def run(self, input_data: dict) -> dict:
        student_data = input_data.get("student_performance", {})
        # Placeholder logic
        return {
            "student_id": student_data.get("student_id", "unknown"),
            "strengths": ["Algebra", "Geometry"],
            "weaknesses": ["Trigonometry"],
            "recommendations": ["Revise Trigonometry basics", "Use visual tools"],
            "progress_score": 0.78
        }
