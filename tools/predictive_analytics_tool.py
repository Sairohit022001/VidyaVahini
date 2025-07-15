from typing import Dict, List

class PredictiveAnalyticsTool:
    def run(self, quiz_results: Dict) -> Dict:
        students = quiz_results.get("students", [])
        if not students:
            return {
                "average_score": 0.0,
                "top_performers": [],
                "weak_areas": [],
                "lesson_plan_suggestions": []
            }

        scores = [student.get("score", 0) for student in students]
        avg_score = sum(scores) / len(scores)

        # Top performers by score (could be capped at 3 or 5)
        top_performers = [
            student.get("name") for student in sorted(
                students, key=lambda x: x.get("score", 0), reverse=True
            )[:5]
        ]

        # Get weak areas from quiz metadata or fallback to empty
        weak_areas = quiz_results.get("weak_areas", [])

        # Basic rule-based lesson suggestions (mock logic)
        lesson_plan_suggestions = [
            f"Re-teach: {concept}" for concept in weak_areas
        ]

        return {
            "average_score": round(avg_score, 2),
            "top_performers": top_performers,
            "weak_areas": weak_areas,
            "lesson_plan_suggestions": lesson_plan_suggestions
        }

predictive_analytics_tool = PredictiveAnalyticsTool()
