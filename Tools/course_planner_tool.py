from typing import Dict

class CoursePlannerTool:
    def run(self, data: Dict):
        current_topic = data.get("current_topic", "Photosynthesis")
        quiz_score = data.get("quiz_score", 70)  # out of 100

        if quiz_score > 85:
            recommended_topic = "Transpiration"
            difficulty = "Advanced"
            adjustment = "up"
        elif quiz_score >= 60:
            recommended_topic = "Plant Nutrition"
            difficulty = "Medium"
            adjustment = "same"
        else:
            recommended_topic = "Reinforce Photosynthesis"
            difficulty = "Beginner"
            adjustment = "down"

        return {
            "current_topic": current_topic,
            "recommended_topic": recommended_topic,
            "reason": f"Based on a quiz score of {quiz_score}, this topic is the best next step.",
            "difficulty_adjustment": adjustment,
            "level": difficulty,
            "suggested_agents": ["QuizAgent", "VisualAgent"],
            "linked_materials": [
                f"https://example.com/resources/{recommended_topic.replace(' ', '_').lower()}"
            ]
        }