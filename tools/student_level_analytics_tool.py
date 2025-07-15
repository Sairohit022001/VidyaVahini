from typing import Dict, List

class StudentLevelAnalyticsTool:
    def run(self, student_performance: Dict) -> Dict:
        name = student_performance.get("name", "unknown")
        quiz_scores = student_performance.get("scores", {})
        concept_scores = student_performance.get("concept_scores", {})

        if not quiz_scores:
            return {
                "student_id": name,
                "strengths": [],
                "weaknesses": [],
                "recommendations": [],
                "progress_score": 0.0
            }

        average_score = sum(quiz_scores.values()) / len(quiz_scores)

        strengths = [topic for topic, score in concept_scores.items() if score >= 80]
        weaknesses = [topic for topic, score in concept_scores.items() if score < 50]
        recommendations = [f"Revise: {topic}" for topic in weaknesses]

        return {
            "student_id": name,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
            "progress_score": round(average_score, 2)
        }

student_level_analytics_tool = StudentLevelAnalyticsTool()