from typing import Dict

class PredictiveAnalyticsTool:
    def run(self, quiz_results: Dict) -> Dict:
        scores = [student["score"] for student in quiz_results.get("students", [])]
        if not scores:
            return {"error": "No quiz results provided."}
        avg_score = sum(scores) / len(scores)
        student_performance= sorted(quiz_results["students"], key=lambda x: x["score"], reverse=True)[:]
        weaknesses = quiz_results.get("weak_areas", [])
        return {
            "average_score": avg_score,
            "top_performers": student_performance,
            "weak_areas": weaknesses,
            "recommendations": "Focus on weak areas for improvement.",
            "future_lessons": "Plan lessons based on class performance trends.",
            "structured_report": {
                "average_score": avg_score,
                "student": [student["name"] for student in student_performance],
                "weak_areas": weaknesses
            } 
        }

predictive_analytics_tool = PredictiveAnalyticsTool()