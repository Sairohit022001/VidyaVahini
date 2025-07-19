from tasks.base import BaseTask
from pydantic import BaseModel, Field
from typing import List

class ClassAnalyticsOutputSchema(BaseModel):
    average_score: float
    top_performers: List[str]
    weak_areas: List[str]
    lesson_plan_suggestions: List[str]

class PredictiveAnalyticsTask(BaseTask):
    name = "GenerateClassAnalytics"
    description = "Analyze class-level quiz performance and suggest lesson improvements."
    inputs = ["quiz_results"]
    output_model = ClassAnalyticsOutputSchema
    output_json = True
    guardrails = { # Ensure guardrails with fallback_response are defined
        "retry_on_fail": 1,
        "fallback_response": {
            "average_score": 0.0,
            "top_performers": [],
            "weak_areas": [],
            "lesson_plan_suggestions": []
        }
    }

    async def run(self, input_data):
        quiz_results = input_data.get("quiz_results", [])

        # Check if quiz_results is not empty before calculating average_score
        if not quiz_results:
            # Return the fallback response directly when no quiz data
            return self.guardrails.get("fallback_response", {
                "average_score": 0.0,
                "top_performers": [],
                "weak_areas": [],
                "lesson_plan_suggestions": []
            })
        else:
            average_score = sum(q["score"] for q in quiz_results) / len(quiz_results)
            top_performers = sorted(quiz_results, key=lambda x: -x["score"])[:3]
            weak_areas = ["Fractions", "Algebra"]  # Just placeholders
            suggestions = ["Revise Algebra basics", "More group practice on Fractions"]

            return {
                "average_score": average_score,
                "top_performers": [s["student_id"] for s in top_performers],
                "weak_areas": weak_areas,
                "lesson_plan_suggestions": suggestions
            }
